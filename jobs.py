from apscheduler.schedulers.blocking import BlockingScheduler
import app

sched = BlockingScheduler()

Hora = 20
minutos = 32

Fuso = -4
Hora_R = Hora - Fuso

# Criar um job que é realizado de X em X horas
@sched.scheduled_job('cron', hour = Hora_R, minute = minutos)
def timed_job():

    print(f"Rodando em {Hora}:{minutos}")

    app.main()
    #app.iconquare()
    pass

sched.start()    