document.addEventListener('DOMContentLoaded', ()=> {
    const alertButton = document.GetElementById('alertButton');
    if(alertButton) alertButton.AddEventListener('click', alertButton_Click)
})

function alertButton_Click(){
    alert("You have pressed the button")
}