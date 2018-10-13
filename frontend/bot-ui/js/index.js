var outputArea = $("#chat-output");

$("#user-input-form").on("submit", function(e) {
  var objDiv = document.getElementById("chat-output");
  objDiv.scrollTop = objDiv.scrollHeight;

  e.preventDefault();
  
  var message_input = $("#user-input").val();
  
  
  outputArea.append(`
    <div class='bot-message'>
      <div class='message'>
        ${message_input}
      </div>
    </div>
  `);


  var output_field="";


  var data = new FormData();
  data.append("message", message_input);

  var xhr = new XMLHttpRequest();

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === 4) {
      console.log(this.responseText);
      output_field=this.responseText;
    }
  });

  xhr.open("POST", "http://127.0.0.1:8000/answer/");
  xhr.send(data);

  setTimeout(function() {
    outputArea.append(`
      <div class='user-message'>
        <div class='message'>
          ${output_field}
        </div>
      </div>
    `);
  }, 3000);
  
  $("#user-input").val("");
  
});