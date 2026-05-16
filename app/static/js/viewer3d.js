/* viewer3d.js — Visualizador 3D completo com OrbitControls */
(function () {
  'use strict';

  if (typeof THREE === 'undefined') return;

  var canvas = document.getElementById('viewer-canvas');
  if (!canvas) return;

  var category = (window.MODELO_CATEGORY || '').toLowerCase();

  var W = canvas.parentElement.clientWidth || 800;
  var H = Math.round(W * 9 / 16);

  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(W, H);
  renderer.setClearColor(0x0f1117, 1);
  renderer.shadowMap.enabled = true;

  var scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0f1117, 0.04);

  var camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 200);
  camera.position.set(8, 6, 10);

  // OrbitControls
  var controls = null;
  if (typeof THREE.OrbitControls !== 'undefined') {
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 1.5, 0);
    controls.update();
  }

  // Iluminação
  scene.add(new THREE.AmbientLight(0x4f8ef7, 0.5));
  var sun = new THREE.DirectionalLight(0xffffff, 1.5);
  sun.position.set(10, 20, 10);
  sun.castShadow = true;
  scene.add(sun);
  var fill = new THREE.DirectionalLight(0xa34ff7, 0.3);
  fill.position.set(-10, 5, -10);
  scene.add(fill);

  // Chão
  var groundMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(30, 30),
    new THREE.MeshLambertMaterial({ color: 0x0a0d1a })
  );
  groundMesh.rotation.x = -Math.PI / 2;
  groundMesh.receiveShadow = true;
  scene.add(groundMesh);
  scene.add(new THREE.GridHelper(30, 30, 0x1a1d2e, 0x1a1d2e));

  // Materiais
  var solidMat = new THREE.MeshLambertMaterial({ color: 0x2a3a5e });
  var wireMat  = new THREE.MeshBasicMaterial({ color: 0x4f8ef7, wireframe: true });
  var accentMat = new THREE.MeshLambertMaterial({ color: 0x4f8ef7 });

  var group = new THREE.Group();
  scene.add(group);

  function addBox(w, h, d, x, y, z, mat) {
    var g = new THREE.BoxGeometry(w, h, d);
    var m = new THREE.Mesh(g, mat || solidMat);
    m.position.set(x, y, z);
    m.castShadow = true;
    group.add(m);
    return m;
  }

  // Construção baseada na categoria
  if (category.includes('estrutural')) {
    // Estrutura de concreto armado — pilares e vigas
    var pillarPos = [[-2,-2],[-2,2],[2,-2],[2,2]];
    pillarPos.forEach(function(p) {
      addBox(0.3, 4, 0.3, p[0], 2, p[1]);
    });
    // Vigas horizontais topo
    addBox(4.3, 0.25, 0.25, 0, 4, -2);
    addBox(4.3, 0.25, 0.25, 0, 4,  2);
    addBox(0.25, 0.25, 4.3, -2, 4, 0);
    addBox(0.25, 0.25, 4.3,  2, 4, 0);
    // Laje
    var laje = new THREE.Mesh(
      new THREE.BoxGeometry(4.3, 0.15, 4.3),
      new THREE.MeshLambertMaterial({ color: 0x3a4a6e, transparent: true, opacity: 0.6 })
    );
    laje.position.set(0, 4.1, 0);
    group.add(laje);
    // Segundo pavimento
    pillarPos.forEach(function(p) {
      addBox(0.3, 3, 0.3, p[0], 5.5, p[1]);
    });
    addBox(4.3, 0.15, 4.3, 0, 7.1, 0);

  } else if (category.includes('arquitetônico') || category.includes('arquitetonico')) {
    // Edifício com fachada envidraçada
    addBox(4, 6, 3, 0, 3, 0);
    // Janelas (planos azuis)
    for (var floor = 0; floor < 3; floor++) {
      for (var col = 0; col < 3; col++) {
        var win = new THREE.Mesh(
          new THREE.PlaneGeometry(0.9, 1.2),
          new THREE.MeshBasicMaterial({ color: 0x4f8ef7, transparent: true, opacity: 0.7, side: THREE.DoubleSide })
        );
        win.position.set(-1.2 + col * 1.2, 1 + floor * 1.8, 1.51);
        group.add(win);
      }
    }
    // Marquise
    addBox(5, 0.15, 1, 0, 0.1, 1.7, accentMat);
    // Cobertura
    addBox(4.4, 0.3, 3.4, 0, 6.15, 0, accentMat);

  } else {
    // Estrutura genérica — galpão industrial
    addBox(6, 0.2, 4, 0, 0.1, 0);
    var cols = [[-2.8,0,-1.8],[-2.8,0,1.8],[2.8,0,-1.8],[2.8,0,1.8],[0,0,-1.8],[0,0,1.8]];
    cols.forEach(function(c) { addBox(0.25, 3.5, 0.25, c[0], 1.75, c[1]); });
    // Vigas do telhado
    for (var i = -3; i <= 3; i += 1.5) {
      addBox(0.15, 0.15, 4.3, i, 3.5, 0, accentMat);
    }
    // Cobertura curva aproximada
    var roofShape = new THREE.Mesh(
      new THREE.CylinderGeometry(2.5, 2.5, 6.5, 16, 1, false, 0, Math.PI),
      new THREE.MeshLambertMaterial({ color: 0x1a2d4e, side: THREE.DoubleSide, transparent: true, opacity: 0.85 })
    );
    roofShape.rotation.z = Math.PI / 2;
    roofShape.position.set(0, 3.5, 0);
    group.add(roofShape);
  }

  // Modo wireframe / sólido
  var wireMode = false;

  function setWireframe(wf) {
    wireMode = wf;
    group.traverse(function(obj) {
      if (obj.isMesh && obj.material && !obj.material.map) {
        obj.material.wireframe = wf;
      }
    });
  }

  var btnWF = document.getElementById('btn-wireframe');
  var btnSolid = document.getElementById('btn-solid');
  var btnReset = document.getElementById('btn-reset');

  if (btnWF)    btnWF.addEventListener('click', function() { setWireframe(true); });
  if (btnSolid) btnSolid.addEventListener('click', function() { setWireframe(false); });
  if (btnReset && controls) {
    btnReset.addEventListener('click', function() {
      camera.position.set(8, 6, 10);
      controls.target.set(0, 1.5, 0);
      controls.update();
    });
  }

  // Loop
  function animate() {
    requestAnimationFrame(animate);
    if (!controls) {
      group.rotation.y += 0.004;
    } else {
      controls.update();
    }
    renderer.render(scene, camera);
  }

  animate();

  window.addEventListener('resize', function() {
    var nw = canvas.parentElement.clientWidth || 800;
    var nh = Math.round(nw * 9 / 16);
    renderer.setSize(nw, nh);
    camera.aspect = nw / nh;
    camera.updateProjectionMatrix();
  });
}());
