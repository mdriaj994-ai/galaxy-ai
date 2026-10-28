import React, { useRef, useEffect } from 'react';

export default function Globe3D() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    let rotationY = 0;
    let rotationX = 0.25;

    // Generate globe vertices (Sphere lat/lon)
    const points = [];
    const radius = 140;
    const lats = 16;
    const lons = 28;

    for (let i = 0; i <= lats; i++) {
      const theta = (i * Math.PI) / lats;
      const sinTheta = Math.sin(theta);
      const cosTheta = Math.cos(theta);

      for (let j = 0; j <= lons; j++) {
        const phi = (j * 2 * Math.PI) / lons;
        const x = radius * sinTheta * Math.cos(phi);
        const y = radius * cosTheta;
        const z = radius * sinTheta * Math.sin(phi);
        points.push({ x, y, z });
      }
    }

    // Active Intelligence Hotspot coordinates on sphere
    const hotspots = [
      { name: 'Silicon Valley', lat: 37.3861, lon: -122.0839, color: '#00F0FF' },
      { name: 'London Core', lat: 51.5074, lon: -0.1278, color: '#7000FF' },
      { name: 'Tokyo Node', lat: 35.6762, lon: 139.6503, color: '#EC4899' },
      { name: 'Singapore Relay', lat: 1.3521, lon: 103.8198, color: '#10B981' },
      { name: 'Dhaka Command', lat: 23.8103, lon: 90.4125, color: '#00F0FF' },
    ].map((h) => {
      const phi = ((h.lon + 180) * Math.PI) / 180;
      const theta = ((90 - h.lat) * Math.PI) / 180;
      return {
        ...h,
        x: radius * Math.sin(theta) * Math.cos(phi),
        y: radius * Math.cos(theta),
        z: radius * Math.sin(theta) * Math.sin(phi),
      };
    });

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;

      // Glow halo behind globe
      const gradient = ctx.createRadialGradient(cx, cy, radius * 0.4, cx, cy, radius * 1.3);
      gradient.addColorStop(0, 'rgba(0, 240, 255, 0.12)');
      gradient.addColorStop(0.7, 'rgba(112, 0, 255, 0.08)');
      gradient.addColorStop(1, 'rgba(11, 14, 20, 0)');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(cx, cy, radius * 1.3, 0, Math.PI * 2);
      ctx.fill();

      // Render wireframe dots
      points.forEach((p) => {
        // Rotate around Y
        const cosY = Math.cos(rotationY);
        const sinY = Math.sin(rotationY);
        const x1 = p.x * cosY + p.z * sinY;
        const z1 = -p.x * sinY + p.z * cosY;

        // Rotate around X
        const cosX = Math.cos(rotationX);
        const sinX = Math.sin(rotationX);
        const y2 = p.y * cosX - z1 * sinX;
        const z2 = p.y * sinX + z1 * cosX;

        // Only draw front-facing points
        if (z2 > -30) {
          const depth = (z2 + radius) / (2 * radius);
          const alpha = Math.max(0.08, depth * 0.45);
          ctx.fillStyle = `rgba(0, 240, 255, ${alpha})`;
          ctx.fillRect(cx + x1, cy + y2, 1.6, 1.6);
        }
      });

      // Render Active Hotspot Nodes with pulsing rings
      hotspots.forEach((h) => {
        const cosY = Math.cos(rotationY);
        const sinY = Math.sin(rotationY);
        const x1 = h.x * cosY + h.z * sinY;
        const z1 = -h.x * sinY + h.z * cosY;

        const cosX = Math.cos(rotationX);
        const sinX = Math.sin(rotationX);
        const y2 = h.y * cosX - z1 * sinX;
        const z2 = h.y * sinX + z1 * cosX;

        if (z2 > 10) {
          ctx.beginPath();
          ctx.fillStyle = h.color;
          ctx.arc(cx + x1, cy + y2, 4, 0, Math.PI * 2);
          ctx.fill();

          ctx.beginPath();
          ctx.strokeStyle = h.color;
          ctx.lineWidth = 1;
          ctx.arc(cx + x1, cy + y2, 8, 0, Math.PI * 2);
          ctx.stroke();

          // Label
          ctx.fillStyle = '#E2E8F0';
          ctx.font = '10px Fira Code';
          ctx.fillText(h.name, cx + x1 + 10, cy + y2 + 3);
        }
      });

      rotationY += 0.007;
      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  return (
    <div className="relative flex items-center justify-center w-full h-[360px] bg-void-card/60 border border-slate-800/80 rounded-2xl overflow-hidden shadow-2xl">
      <div className="absolute top-4 left-4 z-10">
        <span className="text-[10px] font-mono text-cyan-neon uppercase tracking-wider flex items-center">
          <span className="w-1.5 h-1.5 rounded-full bg-cyan-neon animate-ping mr-1.5" />
          3D ORBITAL WIREFRAME RADAR
        </span>
      </div>
      <canvas ref={canvasRef} width={480} height={360} className="w-full max-w-[480px] h-full" />
    </div>
  );
}

