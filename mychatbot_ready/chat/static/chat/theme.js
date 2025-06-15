function toggleTheme() {
    const body = document.body;
    const current = body.dataset.theme || "light";
    const next = current === "light" ? "dark" : "light";
    body.dataset.theme = next;
    localStorage.setItem("theme", next);
}

window.onload = () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.body.dataset.theme = savedTheme;
};
