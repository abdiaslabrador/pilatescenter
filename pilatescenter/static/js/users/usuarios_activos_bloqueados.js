let tecla     = document.querySelector("#caja")
let contenido = document.querySelector('#contenido')
let boleano   = document.getElementById("boolean")

/*
function traer(){
  fetch("http://127.0.0.1:8000/users/UserAPI/")
  .then(function(response){
    if(!response.ok)
     {
        throw new Error(`Error  para conectarse ha lanzado el estatus:  ${response.status}`)
     }
        return response.json();
     })
  .then(function(users){
        usuariosBK = users
        usuarios = usuariosBK
        pintar(usuarios)
        return usuarios
     })
}

traer()
*/

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
          persona = new Persona(rows[i].getElementsByTagName("td")[0].innerHTML, rows[i].getElementsByTagName("td")[1].innerHTML, rows[i].getElementsByTagName("td")[2].innerHTML, rows[i].getElementsByTagName("td")[3].innerHTML, rows[i].getElementsByTagName("td")[4].innerHTML  )
          this.usuariosBK.push(persona)  
        }
    },

    this.pintar = function(usuarios)
    {
      for (let user of usuarios){
          
          if(boleano.innerHTML == "active"){
            contenido.innerHTML +=`
            <tr>
            <td>${user.username}</td>
            <td>${user.first_name}</td>
            <td>${user.last_name}</td>
            <td>${user.ci}</td>
            <td><a class="btn btn-primary"  href="/users/modific_user/${user.id}/">Actualizar</a></td>
            <td><a class="btn btn-bloquear" style="color: white;" href="/users/lock_user/${user.id}/">Bloquear</a></td>
            <td><a class="btn btn-danger"   href="/users/delete_user/${user.id}/">Eliminar</a></td>
            </tr>`
          }
          else if(boleano.innerHTML == "deactive")
          {
            contenido.innerHTML +=`
            <tr>
            <td>${user.username}</td>
            <td>${user.first_name}</td>
            <td>${user.last_name}</td>
            <td>${user.ci}</td>
            <td><a class="btn btn-success"  href="/users/unlock_user/${user.id}/">Desbloquear</a></td>
            <td><a class="btn btn-danger"   href="/users/delete_user/${user.id}/">Eliminar</a></td>
            </tr>` 
          }
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
      this.pintar(this.usuarios)
    }
}

main = new Main()

main.llenar();
function buscar(){
  console.log("es:" + boleano.innerHTML)
  main.buscar();
}