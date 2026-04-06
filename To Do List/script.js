function addTask(){

let taskInput = document.getElementById("taskInput");
let taskText = taskInput.value;

if(taskText === ""){
alert("Enter a task");
return;
}

let li = document.createElement("li");

let checkbox = document.createElement("input");
checkbox.type = "checkbox";

let span = document.createElement("span");
span.textContent = " " + taskText;

checkbox.onclick = function(){

li.classList.add("completed");

document.getElementById("completedList").appendChild(li);

checkbox.disabled = true;

}

li.appendChild(checkbox);
li.appendChild(span);

document.getElementById("pendingList").appendChild(li);

taskInput.value="";
}