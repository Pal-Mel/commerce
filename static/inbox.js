document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);


  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  document.querySelector("form").onsubmit = (event) => {
    event.preventDefault();
    let recepients = document.querySelector("#compose-recipients").value;
    let subject = document.querySelector("#compose-subject").value;
    let body = document.querySelector("#compose-body").value;
    fetch("emails", {
      method: "POST",
      body: JSON.stringify({
        recepients: recepients,
        subject: subject,
        body: body,
      }),
    })
      .then((res) => {
        if (res.status === 201) {
          return {status:true, data:res.json()};
        } else {
          return {status:false, error:res.json()};
        }
      }).catch(er => console.log(er))
      .then((result) => {
        if (result.status) {
          load_mailbox("sent");
          // Clear out composition fields
          document.querySelector("#compose-recipients").value = "";
          document.querySelector("#compose-subject").value = "";
          document.querySelector("#compose-body").value = "";
        } else {
          
          console.log(result)
        }

      })
  };

  
}

function archiveEmail(id, val, mailbox) {
  console.log(mailbox)
  fetch(`emails/${Number(id)}`, {
    method: "PUT",
    body: JSON.stringify({archived:val})
    }).then(() => load_mailbox(mailbox))

    

}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views

  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`emails/${mailbox}`, {
    method: "GET",
  })
    .then((res) => {
      return res.json();
    })
    .then((result) => {
      result.forEach((mail) => {
        const element = document.createElement("div");
        var style = 'display:flex; justify-content: space-between; width: 100%;'
        if (mail.read){style += 'background-color:white; '} else {style += 'background-color:lightgrey; '}
        element.style =style
        element.className = 'card-header border border-secondary rounded-pill m-2'
        element.innerHTML =  ` <div style="display:flex; align-items:center">
                                            <div class="px-2"><strong>Дата: </strong><br><small>${mail.timestamp}</small></div>
                                            <div class="px-2"><strong>Відправник: </strong><br> ${mail.sender} </div>
                                            <div class="px-2"><strong>Тема: </strong><br> ${mail.subject}</div>
                              </div>`
        const buttons = document.createElement('div')
        buttons.style="display:flex;"
         if (mailbox.toUpperCase() == 'INBOX') {
           var button = document.createElement("div")
           button.title = "Архивувати повідомлення"
           button.innerHTML =  `<a onclick=archiveEmail(${mail.id},true,'${mailbox}') class="btn btn-outline-primary m-1"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bag-plus" viewBox="0 0 16 16">
           <path fill-rule="evenodd" d="M8 7.5a.5.5 0 0 1 .5.5v1.5H10a.5.5 0 0 1 0 1H8.5V12a.5.5 0 0 1-1 0v-1.5H6a.5.5 0 0 1 0-1h1.5V8a.5.5 0 0 1 .5-.5z"/>
           <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1zm3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4h-3.5zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V5z"/>
         </svg></a>`
           buttons.appendChild(button)
           button = document.createElement("div")
           button.title = `відповісти ${mail.sender}`
           button.innerHTML =  `<a data-id='${mail}' class="btn btn-outline-primary m-1"> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-reply" viewBox="0 0 16 16">
           <path d="M6.598 5.013a.144.144 0 0 1 .202.134V6.3a.5.5 0 0 0 .5.5c.667 0 2.013.005 3.3.822.984.624 1.99 1.76 2.595 3.876-1.02-.983-2.185-1.516-3.205-1.799a8.74 8.74 0 0 0-1.921-.306 7.404 7.404 0 0 0-.798.008h-.013l-.005.001h-.001L7.3 9.9l-.05-.498a.5.5 0 0 0-.45.498v1.153c0 .108-.11.176-.202.134L2.614 8.254a.503.503 0 0 0-.042-.028.147.147 0 0 1 0-.252.499.499 0 0 0 .042-.028l3.984-2.933zM7.8 10.386c.068 0 .143.003.223.006.434.02 1.034.086 1.7.271 1.326.368 2.896 1.202 3.94 3.08a.5.5 0 0 0 .933-.305c-.464-3.71-1.886-5.662-3.46-6.66-1.245-.79-2.527-.942-3.336-.971v-.66a1.144 1.144 0 0 0-1.767-.96l-3.994 2.94a1.147 1.147 0 0 0 0 1.946l3.994 2.94a1.144 1.144 0 0 0 1.767-.96v-.667z"/>
         </svg> </a>`
           buttons.appendChild(button)
         }
        if (mailbox.toUpperCase() == 'ARCHIVE') {
           var button = document.createElement("div")
           button.title = "Витягти з архіву"
           button.innerHTML =  `<a onclick=archiveEmail(${mail.id},false,'${mailbox}') class="btn btn-outline-primary m-1"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bag-dash" viewBox="0 0 16 16">
           <path fill-rule="evenodd" d="M5.5 10a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1-.5-.5z"/>
           <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1zm3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4h-3.5zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V5z"/>
         </svg></a>`
           buttons.appendChild(button)
        }
        element.appendChild(buttons)
      

        document.querySelector("#emails-view").append(element);
      });
    });
}


