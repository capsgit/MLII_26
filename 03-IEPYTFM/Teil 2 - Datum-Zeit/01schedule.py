import schedule
import time

def job():
    print("Job läuft:", time.strftime("%H:%M:%S"))
print("hola", schedule)
#schedule.every(5).seconds.do(job) #se crea un trabajo/tarea, cada 5 segundos se llamara a la funcion "job()"

print("holis")