/* Ersatzkarte ohne WebGL: bildet die wenigen MapLibre-Funktionen nach, die die App nutzt, auf Basis von Leaflet (Rasterkacheln).
   Zoomstufen werden wie bei MapLibre gezählt (Leaflet-Zoom minus 1). */
(function () {
  const Z = 1;
  const TILES = {
    light: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    dark: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
  };
  const ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions" target="_blank" rel="noopener">CARTO</a>';

  class LngLatBounds {
    constructor(a, b) { this.pts = []; if (a) this.pts.push(a); if (b) this.pts.push(b); }
    extend(c) { this.pts.push(c); return this; }
  }

  class Map {
    constructor(o) {
      this.container = typeof o.container === "string" ? document.getElementById(o.container) : o.container;
      this.L = L.map(this.container, {
        center: [o.center[1], o.center[0]], zoom: o.zoom + Z, minZoom: o.minZoom + Z, maxZoom: o.maxZoom + Z,
        zoomControl: false, zoomAnimation: false, fadeAnimation: false, markerZoomAnimation: false,
        zoomSnap: 0, zoomDelta: 1, wheelPxPerZoomLevel: 90, attributionControl: false,
      });
      L.control.attribution({ prefix: false }).addTo(this.L);
      this.touchZoomRotate = { disableRotation() {} };
      this.overlay = document.createElement("div");
      this.overlay.style.cssText = "position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:450";
      this.container.appendChild(this.overlay);
      this.handlers = {};
      this.markers = new Set();
      ["move", "moveend", "resize", "click"].forEach((ev) => this.L.on(ev, (e) => this._emit(ev === "resize" ? "resize" : ev, e)));
      this.L.on("zoom", () => this._emit("move"));
      this.on("move", () => this.markers.forEach((m) => m._update()));
      this.on("resize", () => this.markers.forEach((m) => m._update()));
      this.tiles = null;
      this.setStyle(o.style);
      this._tileErrors = 0;
    }
    _emit(ev, e) { (this.handlers[ev] || []).forEach((f) => f(e)); }
    on(ev, f) { (this.handlers[ev] = this.handlers[ev] || []).push(f); return this; }
    setStyle(url) {
      const dark = /dark/.test(String(url));
      if (this.tiles) this.tiles.remove();
      this.tiles = L.tileLayer(TILES[dark ? "dark" : "light"], { subdomains: "abcd", maxZoom: 20, attribution: ATTR });
      this.tiles.on("tileerror", () => {
        if (++this._tileErrors === 6) this._emit("error", { error: { message: "Kacheln nicht erreichbar" } });
      });
      this.tiles.addTo(this.L);
    }
    isStyleLoaded() { return true; }
    loaded() { return true; }
    getContainer() { return this.container; }
    getZoom() { return this.L.getZoom() - Z; }
    getCenter() { const c = this.L.getCenter(); return { lng: c.lng, lat: c.lat, toArray: () => [c.lng, c.lat] }; }
    project(c) { const p = this.L.latLngToContainerPoint([c[1], c[0]]); return { x: p.x, y: p.y }; }
    zoomIn() { this.L.zoomIn(); }
    resize() { this.L.invalidateSize(); this._emit("resize"); }
    zoomOut() { this.L.zoomOut(); }
    _target(center, zoom, offset) {
      const z = zoom == null ? this.L.getZoom() : zoom + Z;
      let pt = this.L.project([center[1], center[0]], z);
      if (offset) pt = pt.subtract(L.point(offset[0], offset[1]));
      return { ll: this.L.unproject(pt, z), z };
    }
    flyTo(o) { const t = this._target(o.center, o.zoom, o.offset); this.L.flyTo(t.ll, t.z, { duration: (o.duration || 1000) / 1000 }); }
    easeTo(o) { const t = this._target(o.center, o.zoom, o.offset); this.L.setView(t.ll, t.z, { animate: true, duration: (o.duration || 600) / 1000 }); }
    fitBounds(b, o) {
      const p = (o && o.padding) || {};
      this.L.fitBounds(b.pts.map((c) => [c[1], c[0]]), {
        paddingTopLeft: [p.left || 0, p.top || 0], paddingBottomRight: [p.right || 0, p.bottom || 0],
        maxZoom: o && o.maxZoom != null ? o.maxZoom + Z : undefined, animate: true,
      });
    }
  }

  class Marker {
    constructor(o) { this.el = o.element; this.ll = null; this.map = null; }
    setLngLat(c) { this.ll = c; this._update(); return this; }
    addTo(map) {
      this.map = map; map.markers.add(this);
      this.el.style.cssText += ";position:absolute;left:0;top:0;pointer-events:none;will-change:transform";
      map.overlay.appendChild(this.el); this._update(); return this;
    }
    _update() {
      if (!this.map || !this.ll) return;
      const p = this.map.project(this.ll);
      this.el.style.transform = `translate(${p.x}px,${p.y}px)`;
    }
  }

  window.leafletShim = { Map, Marker, LngLatBounds };
})();
