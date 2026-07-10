import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { isReducedMotion } from '../utils/reduced-motion.js';

class HeroScene {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    this.modelUrl = this.container.getAttribute('data-model-url');
    if (!this.modelUrl) return;

    this.reducedMotion = isReducedMotion();
    this.isVisible = true;
    this.mouseX = 0;
    this.mouseY = 0;
    this.targetMouseX = 0;
    this.targetMouseY = 0;
    this.model = null;
    
    // Check if mobile
    this.isMobile = window.innerWidth < 768;

    this.init();
  }

  init() {
    // Scene
    this.scene = new THREE.Scene();

    // Camera
    this.camera = new THREE.PerspectiveCamera(
      45,
      this.container.clientWidth / this.container.clientHeight,
      0.1,
      100
    );
    this.camera.position.set(0, 0, 5);

    // Renderer
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: "high-performance"
    });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.0;
    this.renderer.domElement.style.width = '100%';
    this.renderer.domElement.style.height = '100%';
    this.renderer.domElement.style.display = 'block';
    this.container.appendChild(this.renderer.domElement);

    // Environment & Lighting (Cinematic Studio Lighting)
    const pmremGenerator = new THREE.PMREMGenerator(this.renderer);
    pmremGenerator.compileEquirectangularShader();
    this.scene.environment = pmremGenerator.fromScene(new RoomEnvironment()).texture;

    // Additional lights for extra "pop"
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
    this.scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0xffffff, 1.5);
    mainLight.position.set(5, 5, 5);
    this.scene.add(mainLight);

    const backLight = new THREE.DirectionalLight(0x7C5CFC, 1.0); // Brand purple
    backLight.position.set(-5, 3, -5);
    this.scene.add(backLight);

    // Load Model using lazy loading / intersection observer
    this.observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        this.loadModel();
        this.observer.disconnect();
      }
    }, { threshold: 0.1 });
    this.observer.observe(this.container);

    // Mouse tracking
    this.container.addEventListener('mousemove', (e) => {
      const rect = this.container.getBoundingClientRect();
      this.targetMouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.targetMouseY = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    });
    this.container.addEventListener('mouseleave', () => {
      this.targetMouseX = 0;
      this.targetMouseY = 0;
    });

    // Resize handling
    window.addEventListener('resize', () => this.onResize());

    // Visibility handling
    document.addEventListener('visibilitychange', () => {
      this.isVisible = !document.hidden;
    });

    // Start animation
    this.clock = new THREE.Clock();
    this.animate();
  }

  loadModel() {
    const loader = new GLTFLoader();
    loader.load(
      this.modelUrl,
      (gltf) => {
        this.model = gltf.scene;
        
        // Center and scale the model automatically
        const box = new THREE.Box3().setFromObject(this.model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        
        const maxDim = Math.max(size.x, size.y, size.z);
        const scale = 2.5 / maxDim; // Adjust 2.5 to fit within the viewport comfortably
        
        this.model.scale.setScalar(scale);
        this.model.position.sub(center.multiplyScalar(scale));
        
        // Add model to a pivot group to fix Blender's Z-up orientation
        const pivot = new THREE.Group();
        pivot.add(this.model);
        pivot.rotation.x = Math.PI / 2; // Stand upright
        
        // Add pivot to the main modelGroup for floating animations
        this.modelGroup = new THREE.Group();
        this.modelGroup.add(pivot);
        this.scene.add(this.modelGroup);
        
        // Enable shadows and enhance materials
        this.model.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            if (child.material) {
              child.material.envMapIntensity = 2.5; // enhance HDR reflection
              child.material.needsUpdate = true;
            }
          }
        });
      },
      undefined,
      (error) => {
        console.error('Error loading GLB model:', error);
      }
    );
  }

  onResize() {
    if (!this.container || !this.camera || !this.renderer) return;

    const width = this.container.clientWidth;
    const height = this.container.clientHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();

    this.renderer.setSize(width, height);
  }

  animate() {
    if (!this.isVisible) {
      requestAnimationFrame(() => this.animate());
      return;
    }

    const time = this.clock.getElapsedTime();

    // Lerp mouse for smooth tracking
    this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
    this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;

    if (this.modelGroup && !this.reducedMotion) {
      // Slow rotation
      this.modelGroup.rotation.y = time * 0.2;
      
      // Gentle floating (sine wave on Y axis)
      this.modelGroup.position.y = Math.sin(time * 1.5) * 0.1;
      
      // Respond subtly to mouse movement
      this.modelGroup.rotation.x = this.mouseY * 0.2;
      this.modelGroup.rotation.z = -this.mouseX * 0.1;
      this.modelGroup.position.x = this.mouseX * 0.2;
    }

    // Render
    this.renderer.render(this.scene, this.camera);

    requestAnimationFrame(() => this.animate());
  }

  dispose() {
    this.isVisible = false;
    
    if (this.observer) {
      this.observer.disconnect();
    }

    if (this.model) {
      this.model.traverse((child) => {
        if (child.isMesh) {
          if (child.geometry) child.geometry.dispose();
          if (child.material) {
            if (Array.isArray(child.material)) {
              child.material.forEach(m => m.dispose());
            } else {
              child.material.dispose();
            }
          }
        }
      });
    }

    this.renderer.dispose();

    if (this.container && this.renderer.domElement) {
      this.container.removeChild(this.renderer.domElement);
    }
  }
}

export function initHeroScene() {
  return new HeroScene('hero-canvas-container');
}

export default HeroScene;
