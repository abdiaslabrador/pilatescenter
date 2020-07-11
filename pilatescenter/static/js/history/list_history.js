let tecla     = document.querySelector("#caja")
let contenido = document.querySelector('#contenido')

let clase_id     = document.querySelector('#lesson_id')

function Lesson(id, day_lesson, hour_lesson, type, cant_max)
{   
  this.id = id; 
  this.day_lesson = day_lesson;
  this.hour_lesson = hour_lesson;
  this.type = type;
  this.cant_max = cant_max;
}

function Main()
{   
    this.lessons  = Array()
    this.lessonsBK = Array()

    this.llenar = function(){
      var rows =document.getElementsByTagName("tbody")[0].rows;
      for(var i=0;i<rows.length;i++){
        console.log(rows[i].getElementsByTagName("td")[0].innerHTML)
          lesson = new Lesson(rows[i].getElementsByTagName("td")[0].innerHTML, rows[i].getElementsByTagName("td")[1].innerHTML, rows[i].getElementsByTagName("td")[2].innerHTML, rows[i].getElementsByTagName("td")[3].innerHTML, rows[i].getElementsByTagName("td")[4].innerHTML  )
          this.lessonsBK.push(lesson)  
        }
    },

    this.pintar = function(lessons)
    {
      for (let lesson of lessons){

            contenido.innerHTML +=`
            <tr>
            <td>${lesson.id}</td>
            <td>${lesson.day_lesson}</td>
            <td>${lesson.hour_lesson}</td>
            <td>${lesson.type}</td>
            <td>${lesson.cant_max}</td>
            <td><a class="btn btn-ver" target="_blank" href="/history/see_history/${lesson.id}/">Ver</a></td>
            <td><a class="btn btn-danger"   href="/history/delete_history/${lesson.id}/">Eliminar</a></td>
            </tr>`
          
      }
    },

    this.buscar = function(){
      contenido.innerHTML = '';
      cadena = tecla.value.toLowerCase().trim()
      this.lessons = this.lessonsBK.filter( (user) => {return( (user.id.toLowerCase().indexOf(cadena) > -1)  || 
                                                       (user.day_lesson.toLowerCase().indexOf(cadena) > -1) ||
                                                       (user.hour_lesson.toLowerCase().indexOf(cadena) > -1) ||
                                                       (user.type.toLowerCase().indexOf(cadena) > -1) ||
                                                       (user.cant_max.toLowerCase().indexOf(cadena) > -1)  
                                                      )
                                             });
       
          this.pintar(this.lessons)
       

    }
}

main = new Main()

main.llenar();


function buscar(){
  
  main.buscar();
}