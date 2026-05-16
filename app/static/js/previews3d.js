/* previews3d.js — Mini-renders 3D nos cards da listagem */
(function () {
  'use strict';

  if (typeof THREE === 'undefined') return;

  var SHAPES = ['box', 'tower', 'galpao', 'pavilhao'];

  document.querySelectorAll('.preview-canvas').forEach(function (canvas, idx) {
    var shape = SHAPES[idx % SHAPES.length];
    buildPreview(canvas, shape);
  });

  function buildPreview(canvas, shape) {
    var W = canvas.parentElement.clientWidth || 200;
    var H = canvas.parentElement.clientHeight || 150;

    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(W, H);
    renderer.setClearColor(0x0f1117, 1);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(50, W / H, 0.1, 100);
    camera.position.set(3, 2.5, 4);
    camera.lookAt(0, 0.5, 0);

    scene.add(new THREE.AmbientLight(0x4f8ef7, 0.7));
    var dl = new THREE.DirectionalLight(0xffffff, 1);
    dl.position.set(4, 8, 6);
    scene.add(dl);

    var mat = new THREE.MeshLambertMaterial({ color: 0x2a3a5e });
    var wmat = new THREE.MeshBasicMaterial({ color: 0x4f8ef7, wireframe: true, opacity: 0.35, transparent: true });

    function addBox(w, h, d, x, y, z) {
      var g = new THREE.BoxGeometry(w, h, d);
      var m = new THREE.Mesh(g, mat);
      m.position.set(x, y, z);
      scene.add(m);
      var mw = new THREE.Mesh(g, wmat);
      mw.position.copy(m.position);
      scene.add(mw);
    }

    if (shape === 'box') {
      addBox(2, 1.5, 1.5, 0, 0.75, 0);
      addBox(0.8, 0.8, 0.8, 1.5, 0.4, 0);
    } else if (shape === 'tower') {
      addBox(1.2, 3, 1.2, 0, 1.5, 0);
      addBox(0.5, 0.6, 0.5, 0, 3.3, 0);
    } else if (shape === 'galpao') {
      addBox(3, 1, 1.5, 0, 0.5, 0);
      var roofG = new THREE.CylinderGeometry(0, 1.6, 0.8, 4);
      var roofM = new THREE.Mesh(roofG, new THREE.MeshLambertMaterial({ color: 0x4f8ef7 }));
      roofM.rotation.y = Math.PI / 4;
      roofM.position.set(0, 1.4, 0);
      scene.add(roofM);
    } else {
      addBox(2.5, 0.8, 1.5, 0, 0.4, 0);
      addBox(0.2, 1.6, 0.2, -1.1, 0.8, -0.6);
      addBox(0.2, 1.6, 0.2, -1.1, 0.8,  0.6);
      addBox(0.2, 1.6, 0.2,  1.1, 0.8, -0.6);
      addBox(0.2, 1.6, 0.2,  1.1, 0.8,  0.6);
    }

    scene.add(new THREE.GridHelper(6, 6, 0x1a1d2e, 0x1a1d2e));

    (function animate() {
      requestAnimationFrame(animate);
      scene.rotation.y += 0.008;
      renderer.render(scene, camera);
    }());
  }
}());
