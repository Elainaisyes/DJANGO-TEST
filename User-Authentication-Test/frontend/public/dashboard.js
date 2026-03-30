(async function protectDashboard() {
    const res = await fetch("http://localhost:8000/api/dashboard/", {
        credentials: "include"
    });

    if (!res.ok) {
        window.location.replace("http://127.0.0.1:5500/User-Authentication-Test/frontend/public/login.html");
    }
})();