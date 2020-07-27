let tecla     = document.querySelector("#caja")
let contenido = document.querySelector('#contenido')

let clase_id     = document.querySelector('#lesson_id')

function Persona(id, username, first_name, last_name, ci)
{   this.id = id;  
    this.username = username;
    this.first_name = first_name;
    this.last_name = last_name;
    this.ci = ci
}

function Main()
{   
    this.usuarios  = Array()
    this.usuariosBK = Array()

    this.llenar = function(){
      var rows =document.getElementsByTagName("tbody")[0].rows;
      for(var i=0;i<rows.length;i++){
        console.log(rows[i].getElementsByTagName("td")[0].innerHTML)
          persona = new Persona(rows[i].getElementsByTagName("td")[0].innerHTML, rows[i].getElementsByTagName("td")[1].innerHTML, rows[i].getElementsByTagName("td")[2].innerHTML, rows[i].getElementsByTagName("td")[3].innerHTML, rows[i].getElementsByTagName("td")[4].innerHTML  )
          this.usuariosBK.push(persona)  
        }
      contenido.innerHTML = '';
    },

    this.pintar = function(usuarios)
    {
      for (let user of usuarios){

            contenido.innerHTML +=`
            <tr>
            <td>${user.username}</td>
            <td>${user.first_name}</td>
            <td>${user.last_name}</td>
            <td>${user.ci}</td>
            <td><a class="btn btn-success"  href="/lesson/add_to_lesson/${clase_id.innerHTML}/${user.id}/">Añadir</a></td>
            </tr>`
          
      }
    },

    this.buscar = function(){
      contenido.innerHTML = '';
      cadena = tecla.value.toLowerCase().trim()
      this.usuarios = this.usuariosBK.filter( (user) => {return( (user.username.toLowerCase().indexOf(cadena) > -1)  || 
                                                       (user.first_name.toLowerCase().indexOf(cadena) > -1) ||
                                                       (user.last_name.toLowerCase().indexOf(cadena) > -1) ||
                                                       (user.ci.toLowerCase().indexOf(cadena) > -1)  
                                                      )
                                             });
       if(tecla.value != '')
       {
          this.pintar(this.usuarios)
       }

    }
}

main = new Main()

main.llenar();


function buscar(){
  
  main.buscar();
}