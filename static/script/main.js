// navbar toggler - - - - -
const toggler = document.querySelector(".nav__toggler");
const navbar = document.querySelector(".header");
toggler.addEventListener("click", (e) => {
  navbar.classList.toggle("nav__expanded");
});

const loginBtn = document.querySelector(".login .title");
const login = document.querySelector(".login");
const signupBtn = document.querySelector(".signup .title");
const signup = document.querySelector(".signup");
loginBtn.addEventListener("click", () => {
  login.classList.toggle("slide-up");
  signup.classList.toggle("slide-up");
});

signupBtn.addEventListener("click", () => {
  login.classList.toggle("slide-up");
  signup.classList.toggle("slide-up");
});