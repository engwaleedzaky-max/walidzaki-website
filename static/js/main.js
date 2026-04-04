const langToggle = document.getElementById("langToggle");

if (langToggle) {
  langToggle.addEventListener("click", () => {
    const currentLang = document.documentElement.lang === "en" ? "en" : "ar";
    const nextLang = currentLang === "ar" ? "en" : "ar";
    const url = new URL(window.location.href);
    url.searchParams.set("lang", nextLang);
    window.location.href = url.toString();
  });
}
