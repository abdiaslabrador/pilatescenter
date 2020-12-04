from apscheduler.schedulers.blocking import BlockingScheduler
import psycopg2

from datetime import datetime
import pytz


TIME_ZONE =     'America/Caracas' #'UTC'
ENABLE      = '---'
NOTCHANCE   = 'NO CHANCE'
INPROCESS   = 'EN CLASE'
FINISHED    = 'FINALIZADO'


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def updateTable():
    my_date = datetime.now(pytz.timezone(TIME_ZONE))
    print(my_date.date(), " ", my_date.time())
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="****",
                                      host="localhost",
                                      port="5432",
                                      database="pilatescenter")

        cursor = connection.cursor()

        sql_select_query ="""
                                update lesson_det_lesson_det
                                set lesson_status = 
                                       case
                                       when  EXTRACT(HOUR FROM hour_chance) = %s and EXTRACT(MINUTE FROM hour_chance) = %s 
                                            then %s
                                       when  EXTRACT(HOUR FROM hour_lesson) = %s and EXTRACT(MINUTE FROM hour_lesson) = %s 
                                            then %s
                                       when  EXTRACT(HOUR FROM hour_end) = %s and EXTRACT(MINUTE FROM hour_end) = %s 
                                            then %s
                                       end
                                WHERE reset= False
                                      and day_lesson = %s
                                      AND
                                      case
                                       when  EXTRACT(HOUR FROM hour_chance) = %s and EXTRACT(MINUTE FROM hour_chance) = %s 
                                            then %s
                                       when  EXTRACT(HOUR FROM hour_lesson) = %s and EXTRACT(MINUTE FROM hour_lesson) = %s
                                            then %s
                                       when  EXTRACT(HOUR FROM hour_end) = %s and EXTRACT(MINUTE FROM hour_end) = %s 
                                            then %s
                                       end is not null

                                       RETURNING id, lesson_status

                          """
    

        cursor.execute(sql_select_query, (my_date.hour, my_date.minute, NOTCHANCE,
                                          my_date.hour, my_date.minute, INPROCESS,
                                          my_date.hour, my_date.minute, FINISHED,
                                          my_date.date(),
                                          my_date.hour, my_date.minute, NOTCHANCE,
                                          my_date.hour, my_date.minute, INPROCESS,
                                          my_date.hour, my_date.minute, FINISHED,
                                          )
                       )

        connection.commit()
        records = cursor.fetchall()
        print(records)
        for record in records:
            if record[1] == FINISHED:
                sql_select_query="""
                                    update devolution_devolution 
                                    set returned = true
                                    from devolution_devolution_id_lesson_fk as m2m_devolution_lesson, lesson_det_lesson_det as lesson_det
                                    where %s = m2m_devolution_lesson.lesson_det_id
                                    and m2m_devolution_lesson.devolution_id = devolution_devolution.id
                                """
                cursor.execute(sql_select_query, (record[0],))
                connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

sched.start()