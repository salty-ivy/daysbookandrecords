document.addEventListener("DOMContentLoaded", () => {
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );

  $navbarBurgers.forEach((el) => {
    el.addEventListener("click", () => {
      const target = el.dataset.target;
      const $target = document.getElementById(target);
      el.classList.toggle("is-active");
      $target.classList.toggle("is-active");
      const navbarLinks = document.querySelectorAll('.is-uppercase');
      navbarLinks.forEach(link => {
        link.classList.toggle('px-6');
      });
    });
  });
  const allDropdowns = document.querySelectorAll(
    ".navbar-item.has-dropdown"
  );

  allDropdowns.forEach((dropdown) => {
    const dropdownToggle = dropdown.querySelector('.dropdown-toggle');
    dropdownToggle.addEventListener("click", (event) => {
      event.preventDefault();

      const elem = dropdown.querySelector(".navbar-dropdown");
      elem.classList.toggle("is-active");
    });
  });
});
