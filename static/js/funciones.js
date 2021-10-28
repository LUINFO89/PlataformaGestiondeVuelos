//FUNCION RESERVAS
function guardar(){
    document.getElementById("IdFormulario").action="/reservas/guardar/";
}
function visualizar(){
    document.getElementById("IdFormulario").action="/reservas/visualizar/";
}
function eliminar(){
    document.getElementById("IdFormulario").action="/reservas/eliminar/";
}
function actualizar(){
    document.getElementById("IdFormulario").action="/reservas/actualizar/";
}
//FUNCIONES VUELOS
function guardarV(){
    document.getElementById("IdFormularioV").action="/vuelos/guardar/";
}
function visualizarV(){
    document.getElementById("IdFormularioV").action="/vuelos/visualizar/";
}
function eliminarV(){
    document.getElementById("IdFormularioV").action="/vuelos/eliminar/";
}
function actualizarV(){
    document.getElementById("IdFormularioV").action="/vuelos/actualizar/";
}
//FUNCIONES COMENTARIOS
function guardarC(){
    document.getElementById("IdFormularioC").action="/comentarios/guardar/";
}
function visualizarC(){
    document.getElementById("IdFormularioC").action="/comentarios/visualizar/";
}
function eliminarC(){
    document.getElementById("IdFormularioC").action="/comentarios/eliminar/";
}
function actualizarC(){
    document.getElementById("IdFormularioC").action="/comentarios/actualizar/";
}

//FUNCIONES USUARIOS
function guardarU(){
    document.getElementById("IdFormularioU").action="/usuarios/guardar/";
}
function visualizarU(){
    document.getElementById("IdFormularioU").action="/usuarios/visualizar/";
}
function eliminarU(){
    document.getElementById("IdFormularioU").action="/usuarios/eliminar/";
}
function actualizarU(){
    document.getElementById("IdFormularioU").action="/usuarios/actualizar/";
}