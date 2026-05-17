from controller import Robot

# =========================================================
# AGV LINE FOLLOWER PID
# ROUTE A FINAL - POSITION INDEPENDENT
# DOMINAN KIRI - BEL0K KIRI DI INTERSECTION 1
# =========================================================

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# =========================================================
# SENSOR & MOTOR
# =========================================================
sensors = []
for i in range(8):
    sensor = robot.getDevice(f'PS{i}')
    sensor.enable(timestep)
    sensors.append(sensor)

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0)
right_motor.setVelocity(0)

# =========================================================
# PARAMETER PID & KECEPATAN
# =========================================================
Kp = 0.45
Kd = 0.08
last_error = 0

NORMAL_SPEED = 1.6
PREPARE_SPEED = 0.8
TURN_SPEED = 0.7
MAX_SPEED = 4.0

threshold = 120

# =========================================================
# STATE MACHINE & NODE SYSTEM
# =========================================================
# State 0: Belum naik ke jalur atas (Abaikan intersection dulu)
# State 1: Sudah naik, siap merespon Intersection 1
lintasan_state = 0 

node_count = 0
node_lock = 0
turn_mode = 0
turn_timer = 0
TURN_DURATION = 16

# =========================================================
# MAIN LOOP
# =========================================================
while robot.step(timestep) != -1:
    biner = ""
    error = 0
    jumlah_kena = 0

    # Baca Sensor
    for i in range(8):
        val = sensors[i].getValue()
        if val < threshold:
            biner += "0"
            error += (i - 3.5)
            jumlah_kena += 1
        else:
            biner += "1"

    # Deteksi Tikungan Kiri Pertama untuk Menanjak ke Atas
    if error < -2.5 and lintasan_state == 0:
        lintasan_state = 1
        print("=== ROBOT MEMASUKI JALUR UTAMA ATAS ===")

    # Debug Monitor
    print(
        "ROUTE A RUNNING",
        "| State:", lintasan_state,
        "| Node:", node_count,
        "| Biner:", biner
    )

    # Antisipasi tikungan (Perlambatan)
    if (biner == "01111111" or biner == "11111110"):
        current_speed = PREPARE_SPEED
    else:
        current_speed = NORMAL_SPEED

    # =====================================================
    # DETEKSI NODE INTERSECTION
    # =====================================================
    if biner == "11111111" and node_lock == 0:
        node_lock = 1
        
        if lintasan_state == 1:
            node_count += 1

            # INTERSECTION 1 -> AMBIL JALUR KIRI (ROUTE A)
            if node_count == 1:
                turn_mode = 2  # Aktifkan mode belok kiri
                turn_timer = TURN_DURATION
                print(">>> INTERSECTION 1: BELOK KIRI KE ROUTE A")

    # =====================================================
    # RESET SYSTEM SIKLUS LAP
    # =====================================================
    if biner == "00111100":
        node_lock = 0
        
        # Reset siklus jika robot sudah melewati Route A bawah dan kembali ke garis lurus
        if node_count >= 1 and turn_mode == 0:
            node_count = 0
            lintasan_state = 0  # Bersiap mendeteksi tanjakan kiri lagi di lap berikutnya
            print("=== SIKLUS LAP A SELESAI, RE-CALIBRATION POSITION ===")

    # =====================================================
    # EKSEKUSI BELOK KIRI PAKSA
    # =====================================================
    if turn_mode == 2:
        left_motor.setVelocity(1.0)
        right_motor.setVelocity(0.2)
        
        turn_timer -= 1
        if turn_timer <= 0:
            turn_mode = 0
        continue

    # =====================================================
    # PID RUNNING NORMAL
    # =====================================================
    if jumlah_kena > 0:
        avg_error = error / jumlah_kena
        derivative = avg_error - last_error
        diff = (Kp * avg_error) + (Kd * derivative)
        last_error = avg_error

        if diff > 1.8: diff = 1.8
        if diff < -1.8: diff = -1.8

        speed = TURN_SPEED if abs(avg_error) > 2 else current_speed
        left_speed = speed - diff
        right_speed = speed + diff

        left_speed = max(min(left_speed, MAX_SPEED), -MAX_SPEED)
        right_speed = max(min(right_speed, MAX_SPEED), -MAX_SPEED)

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
        
    else:
        # Lost Line Recovery (Sistem keamanan jika slip keluar garis)
        left_motor.setVelocity(1.2)
        right_motor.setVelocity(0.2)  