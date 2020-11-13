function clicker(arg){
    if(arg=="happ"){
        document.querySelector("#happ").classList.add("active");
        document.querySelector("#es").classList.remove("active");
    }
    else if(arg=="es"){
        document.querySelector("#es").classList.add("active");
        document.querySelector("#happ").classList.remove("active");
    }
}