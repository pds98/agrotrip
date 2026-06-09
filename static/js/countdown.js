/* AgroTrip — compte à rebours pour les AgroTrips à venir */

document.addEventListener("DOMContentLoaded", function () {
  const compteurs = document.querySelectorAll(".countdown");
  if (!compteurs.length) return;

  function pad(n) { return String(n).padStart(2, "0"); }

  function tick() {
    const maintenant = new Date().getTime();

    compteurs.forEach(c => {
      const cible = new Date(c.dataset.date).getTime();
      let diff = cible - maintenant;

      const elDays = c.querySelector('[data-unit="days"]');
      const elHours = c.querySelector('[data-unit="hours"]');
      const elMin = c.querySelector('[data-unit="minutes"]');
      const elSec = c.querySelector('[data-unit="seconds"]');

      if (diff <= 0) {
        c.classList.add("finie");
        if (elDays) elDays.textContent = "00";
        if (elHours) elHours.textContent = "00";
        if (elMin) elMin.textContent = "00";
        if (elSec) elSec.textContent = "00";
        return;
      }

      const jours = Math.floor(diff / 86400000);
      diff -= jours * 86400000;
      const heures = Math.floor(diff / 3600000);
      diff -= heures * 3600000;
      const minutes = Math.floor(diff / 60000);
      diff -= minutes * 60000;
      const secondes = Math.floor(diff / 1000);

      if (elDays) elDays.textContent = pad(jours);
      if (elHours) elHours.textContent = pad(heures);
      if (elMin) elMin.textContent = pad(minutes);
      if (elSec) elSec.textContent = pad(secondes);
    });
  }

  tick();
  setInterval(tick, 1000);
});
