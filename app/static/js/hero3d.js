/* hero3d.js — Animação 3D da página inicial */
(function () {
  'use strict';

  var canvas = document.getElementById('hero-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  var W = canvas.parentElement.clientWidth || 400;
  var H = W;

  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(W, H);
  renderer.setClearColor(0x000000, 0);

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(5, 4, 7);
  camera.lookAt(0, 1, 0);

  // Iluminação
  scene.add(new THREE.AmbientLight(0x4f8ef7, 0.6));
  var dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
  dirLight.position.set(5, 10, 7);
  scene.add(dirLight);

  // Paleta
  var C = {
    base:   0x1a1d2e,
    wall:   0x2a3a5e,
    roof:   0x4f8ef7,
    wire:   0x4f8ef7,
    ground: 0x0f1117,
  };

  // Chão
  var ground = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshLambertMaterial({ color: C.ground })
  );
  ground.rotation.x = -Math.PI / 2;
  scene.add(ground);

  // Grid no chão
  var grid = new THREE.GridHelper(10, 10, C.wire, C.base);
  grid.material.opacity = 0.4;
  grid.material.transparent = true;
  scene.add(grid);

  // Construção principal
  var buildingMat = new THREE.MeshLambertMaterial({ color: C.wall });

  function box(w, h, d, x, y, z) {
    var m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), buildingMat);
    m.position.set(x, y, z);
    scene.add(m);
    // wireframe overlay
    var wf = new THREE.Mesh(
      new THREE.BoxGeometry(w, h, d),
      new THREE.MeshBasicMaterial({ color: C.wire, wireframe: true, opacity: 0.3, transparent: true })
    );
    wf.position.copy(m.position);
    scene.add(wf);
    return m;
  }

  // Corpo principal
  box(3, 2, 2, 0, 1, 0);
  // Telhado / laje inclinada
  var roofGeo = new THREE.ConeGeometry(2.2, 1.2, 4);
  var roofMat = new THREE.MeshLambertMaterial({ color: C.roof });
  var roof = new THREE.Mesh(roofGeo, roofMat);
  roof.rotation.y = Math.PI / 4;
  roof.position.set(0, 2.6, 0);
  scene.add(roof);
  // Extensão lateral
  box(1.5, 1.2, 1.5, 2.2, 0.6, 0);
  // Coluna esquerda
  box(0.2, 2, 0.2, -1.7, 1, -0.7);
  box(0.2, 2, 0.2, -1.7, 1,  0.7);

  function animate() {
    requestAnimationFrame(animate);
    scene.rotation.y += 0.005;
    renderer.render(scene, camera);
  }

  animate();

  window.addEventListener('resize', function () {
    var nw = canvas.parentElement.clientWidth || 400;
    renderer.setSize(nw, nw);
  });
}());
