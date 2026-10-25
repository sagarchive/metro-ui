/* metro.js - behaviour for the Windows Phone 8.1 kit. No dependencies.
   Include after metro.css. Everything is opt-in via data attributes / classes.
   Timings (ms): press tilt 70 in / 160 out; turnstile rows out 128, in 180, stagger 33, gap 120. */
(function () {
  "use strict";
  var TILT = { deg: 14, inMs: 70, outMs: 160, fov: 500 };
  var TURN = { outMs: 128, inMs: 180, stagger: 33, gap: 120, outDeg: 50, inDeg: 80 };

  /* Press tilt: the surface leans away from the finger (14 deg max), no ripple, no colour fade. */
  function tilt(el) {
    var rect;
    function set(e, ms) {
      rect = rect || el.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width - 0.5;
      var y = (e.clientY - rect.top) / rect.height - 0.5;
      var dead = 0.25;
      var rx = Math.abs(y) < dead ? 0 : -Math.sign(y) * TILT.deg;
      var ry = Math.abs(x) < dead ? 0 : Math.sign(x) * TILT.deg;
      el.style.transition = "transform " + ms + "ms cubic-bezier(.1,.9,.2,1)";
      el.style.transform = "perspective(" + TILT.fov + "px) rotateX(" + rx + "deg) rotateY(" + ry + "deg) scale(.96)";
    }
    function release() {
      rect = null;
      el.style.transition = "transform " + TILT.outMs + "ms cubic-bezier(.1,.9,.2,1)";
      el.style.transform = "";
    }
    el.addEventListener("pointerdown", function (e) { set(e, TILT.inMs); });
    ["pointerup", "pointercancel", "pointerleave"].forEach(function (t) { el.addEventListener(t, release); });
  }

  /* Toggle: the whole row is the hit target; the thumb jumps (no slide); the state label flips On/Off. */
  function toggleRow(row) {
    var tg = row.querySelector(".m-toggle");
    var state = row.querySelector(".s");
    if (!tg) return;
    row.addEventListener("click", function () {
      var on = tg.classList.toggle("on");
      if (state) state.textContent = on ? "On" : "Off";
      row.dispatchEvent(new CustomEvent("metro:toggle", { detail: { on: on }, bubbles: true }));
    });
  }

  /* Slider: drag anywhere on the block; value 0..100, square thumb, fill = accent. */
  function slider(el) {
    var track = el.querySelector(".track"), fill = el.querySelector(".fill"),
        thumb = el.querySelector(".thumb"), pct = el.querySelector(".pct");
    function put(v) {
      v = Math.max(0, Math.min(100, Math.round(v)));
      fill.style.width = v + "%";
      thumb.style.left = "calc(" + v + "% - 5px)";
      if (pct) pct.textContent = v + "%";
      el.dataset.value = v;
      el.dispatchEvent(new CustomEvent("metro:slide", { detail: { value: v }, bubbles: true }));
    }
    function move(e) { var r = track.getBoundingClientRect(); put((e.clientX - r.left) / r.width * 100); }
    el.addEventListener("pointerdown", function (e) {
      el.setPointerCapture(e.pointerId); move(e);
      el.addEventListener("pointermove", move);
    });
    el.addEventListener("pointerup", function () { el.removeEventListener("pointermove", move); });
    put(parseFloat(el.dataset.value || "50"));
  }

  /* Turnstile: rows rotate about their left edge. Out: top-down, 128 ms, 50 deg. In: 180 ms from 80 deg. */
  function turnstile(rows, dir, done) {
    var list = Array.prototype.slice.call(rows);
    var out = dir === "out";
    list.forEach(function (r, i) {
      r.style.transformOrigin = "0 50%";
      r.style.transition = "none";
      r.style.opacity = out ? 1 : 0;
      r.style.transform = out ? "none" : "perspective(600px) rotateY(" + (-TURN.inDeg) + "deg)";
      void r.offsetWidth;
      setTimeout(function () {
        r.style.transition = "transform " + (out ? TURN.outMs : TURN.inMs) + "ms " +
          (out ? "cubic-bezier(.5,0,1,.6)" : "cubic-bezier(.1,.9,.2,1)") + ",opacity " + (out ? TURN.outMs : TURN.inMs) + "ms linear";
        r.style.transform = out ? "perspective(600px) rotateY(" + (-TURN.outDeg) + "deg)" : "none";
        r.style.opacity = out ? 0 : 1;
      }, i * TURN.stagger);
    });
    var total = (list.length - 1) * TURN.stagger + (out ? TURN.outMs : TURN.inMs);
    if (done) setTimeout(done, total + (out ? TURN.gap : 0));
  }

  /* Pivot: tap the dimmed next title to slide; inactive titles sit at 40 % opacity. */
  function pivot(el) {
    var titles = el.querySelectorAll("[data-pivot]");
    titles.forEach(function (t) {
      t.addEventListener("click", function () {
        titles.forEach(function (o) { o.style.opacity = o === t ? 1 : 0.4; });
        el.dispatchEvent(new CustomEvent("metro:pivot", { detail: { name: t.dataset.pivot }, bubbles: true }));
      });
    });
  }

  function init(root) {
    root = root || document;
    root.querySelectorAll("[data-tilt], .m-tile, .m-entry, .m-switch, .m-round, .m-button, .m-kbd .k").forEach(tilt);
    root.querySelectorAll(".m-switch").forEach(toggleRow);
    root.querySelectorAll(".m-slider").forEach(slider);
    root.querySelectorAll("[data-pivot-group]").forEach(pivot);
  }

  window.Metro = { init: init, turnstile: turnstile, tilt: tilt, TILT: TILT, TURN: TURN };
  if (document.readyState !== "loading") init(); else document.addEventListener("DOMContentLoaded", function () { init(); });
})();
