  const registerForm = document.getElementById("registerForm");
  const loginForm = document.getElementById("loginForm");
  const logoutButton = document.getElementById("logoutButton");
  const loadDashboardButton = document.getElementById('loadDataButton');

  if (registerForm) {
    registerForm.addEventListener("submit", (event) => {register(event)});
  }

  if (loginForm) {
    loginForm.addEventListener("submit", (event) => {login(event)});
  }

  if (logoutButton) {
    logoutButton.addEventListener("click", logout);
  }

  if (loadDashboardButton) {
    loadDashboardButton.addEventListener("click", loadUser);
  }

async function register(event) {
    event.preventDefault();
    const username = document.getElementById('usernameInput').value;
    const password = document.getElementById('passwordInput').value;

    const response = await fetch(
        'http://localhost:8000/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        }
    );

    const text = await response.text();
    if (!response.ok) {
        alert(text);
        return;
    }

    window.location.replace('login.html')
}

async function login (event) {
    event.preventDefault();
    const username = document.getElementById('usernameInput').value;
    const password = document.getElementById('passwordInput').value;

    const response = await fetch("http://localhost:8000/api/login/", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        credentials: 'include',
        // credentials: include tells the program to include cookies. We use cookies to track access tokens.
        body: JSON.stringify({username,password})
    });

    event.target.reset();
    const text = await response.text();

    if(!response.ok) {
        alert(text);
        return;
    }

    window.location.replace('http://127.0.0.1:5500/User-Authentication-Test/frontend/private/dashboard.html');
}

async function loadUser() {
    const res = await fetch('http://localhost:8000/api/dashboard/', {
        method: 'GET',
        credentials: 'include'
    });

    if (!res.ok) {
        window.location.replace('/login.html');
        return;
    }
    
    const data = await res.json();
    const username = data?.username || "User";

    document.getElementById('result').innerText = 
        `Welcome ${username}`;
}

async function logout() {
    await fetch('http://localhost:8000/api/logout/', {
        method: 'POST',
        credentials: 'include'
    });

    window.location.replace('http://127.0.0.1:5500/User-Authentication-Test/frontend/public/login.html');
}

async function getNewAccessToken () {
    const res = await fetch('http://localhost:8000/api/refresh/', {
        method: 'POST',
        credentials: 'include'
    });

    const data = await res.json();
    return data.access
}