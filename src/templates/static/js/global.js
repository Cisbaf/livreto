window.addEventListener("DOMContentLoaded", ()=>{
    const alerts = document.querySelectorAll(".alertDesign");
    for (var x = 0; x < alerts.length; x++){
            const alert = alerts[x];
            setTimeout(()=>{
                alert.remove();
            }, 5000)
    }
})