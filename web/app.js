/**
 * JARVIS Universal Voice Dashboard - Frontend Controller
 * MediaRecorder + Hardware Mic + WebSpeech মাল্টি-মোড ফুল সাপোর্ট
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const btnToggleMic    = document.getElementById('btn-toggle-mic');
    const micStatusText   = document.getElementById('mic-status-text');
    const pulseContainer  = document.getElementById('pulse-container');
    const liveSpeechText  = document.getElementById('live-speech-text');
    const jarvisOutput    = document.getElementById('jarvis-speech-output');
    const aiStatusTag     = document.getElementById('ai-status-tag');
    const langSelect      = document.getElementById('lang-select');
    const micModeSelect   = document.getElementById('mic-mode-select');
    const textForm        = document.getElementById('text-command-form');
    const manualInput     = document.getElementById('manual-command-input');
    const logContainer    = document.getElementById('log-container');
    const btnClearLogs    = document.getElementById('btn-clear-logs');
    const btnForceRun     = document.getElementById('btn-force-run');
    const speechBadge     = document.getElementById('speech-state-badge');
    const canvas          = document.getElementById('audio-wave-canvas');
    const ctx             = canvas.getContext('2d');

    let isListening       = false;
    let animFrameId       = null;
    let silenceTimer      = null;
    let isExecuting       = false;

    // MediaRecorder Variables
    let mediaStream       = null;
    let mediaRecorder     = null;
    let audioChunks       = [];
    let audioCtx          = null;
    let analyser          = null;
    let silenceCheckId    = null;
    let speechStarted     = false;
    let silenceStartTime  = null;

    // Web Speech API
    let recognition       = null;
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

    // ────────────────────────────────────────────────────────
    // 🎙️ Mode 1: HTML5 MediaRecorder (AdsPower, Chrome, Edge)
    // ────────────────────────────────────────────────────────
    async function startMediaRecording() {
        try {
            audioChunks = [];
            speechStarted = false;
            silenceStartTime = null;

            mediaStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });

            // Audio Context for Visualization & Silence Detection
            try {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioCtx.createAnalyser();
                analyser.fftSize = 256;
                const source = audioCtx.createMediaStreamSource(mediaStream);
                source.connect(analyser);
            } catch(e) {
                console.log('AudioContext init notice:', e);
            }

            const mimeTypes = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/wav', ''];
            let chosenMime = '';
            for (let m of mimeTypes) {
                if (!m || MediaRecorder.isTypeSupported(m)) { chosenMime = m; break; }
            }

            mediaRecorder = chosenMime ? new MediaRecorder(mediaStream, { mimeType: chosenMime }) : new MediaRecorder(mediaStream);

            mediaRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) audioChunks.push(e.data);
            };

            mediaRecorder.onstop = async () => {
                stopVisuals();
                if (silenceCheckId) { clearInterval(silenceCheckId); silenceCheckId = null; }
                if (mediaStream) {
                    mediaStream.getTracks().forEach(t => t.stop());
                    mediaStream = null;
                }

                if (audioChunks.length === 0) {
                    setBadge('কোনো কথা পাওয়া যায়নি', '');
                    liveSpeechText.textContent = '❌ কোনো সাউন্ড রেকর্ড হয়নি। আবার চেষ্টা করুন।';
                    return;
                }

                const blob = new Blob(audioChunks, { type: mediaRecorder.mimeType || 'audio/webm' });
                await sendAudioBlobToBackend(blob);
            };

            mediaRecorder.start(250);
            isListening = true;
            btnToggleMic.classList.add('active');
            pulseContainer.classList.add('listening');
            micStatusText.textContent = 'রেকর্ড হচ্ছে... (শেষ হলে ক্লিক করুন)';
            liveSpeechText.textContent = '🎙️ আপনার কথা শুনছি... বলুন (কথা শেষ হলে মাইকে আবার ক্লিক করুন)';
            setBadge('রেকর্ড হচ্ছে...', 'active');
            startVisualizer();
            addLog('MIC', 'মাইক্রোফোন চালু — কথা বলুন');

            // Silence detector: কথা শেষ হলে ১.২ সেকেন্ডে অটো সাবমিট
            if (analyser) {
                const dataArr = new Uint8Array(analyser.frequencyBinCount);
                silenceCheckId = setInterval(() => {
                    analyser.getByteFrequencyData(dataArr);
                    let sum = 0;
                    for (let i = 0; i < dataArr.length; i++) sum += dataArr[i];
                    const avg = sum / dataArr.length;

                    if (avg > 18) {
                        speechStarted = true;
                        silenceStartTime = null;
                    } else if (speechStarted && avg < 12) {
                        if (!silenceStartTime) {
                            silenceStartTime = Date.now();
                        } else if (Date.now() - silenceStartTime > 1400) {
                            // ১.৪ সেকেন্ড নীরব থাকলে অটো সাবমিট
                            stopMediaRecording();
                        }
                    }
                }, 100);
            }

        } catch (err) {
            console.error('Mic access error:', err);
            jarvisOutput.textContent = '❌ মাইক্রোফোন অ্যাক্সেস করতে সমস্যা! ব্রাউজারের তালার আইকনে ক্লিক করে Microphone "Allow" করুন।';
            addLog('ERROR', 'মাইক্রোফোন পারমিশন দিন: ' + err.message);
            stopVisuals();
        }
    }

    function stopMediaRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            try { mediaRecorder.stop(); } catch(e){}
        }
        isListening = false;
    }

    async function sendAudioBlobToBackend(audioBlob) {
        if (isExecuting) return;
        isExecuting = true;
        setBadge('প্রসেসিং...', 'executing');
        aiStatusTag.textContent = 'কথা বিশ্লেষণ হচ্ছে...';
        aiStatusTag.style.color = '#ffb800';
        liveSpeechText.textContent = '🔄 আপনার কথা গুগল এআই দিয়ে প্রসেস হচ্ছে...';

        try {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'voice.webm');

            const res = await fetch('/api/voice_upload?lang=' + encodeURIComponent(langSelect.value), {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            if (data.transcript) {
                liveSpeechText.textContent = '✅ ' + data.transcript;
                addLog('USER', `"${data.transcript}"`);
            } else {
                liveSpeechText.textContent = data.reply || 'কথা শনাক্ত করা যায়নি।';
            }

            if (data.reply) {
                jarvisOutput.textContent = data.reply;
                playBengaliAudio(data.reply);
                addLog('JARVIS', data.reply);
            }

            if (data.url) {
                try { window.open(data.url, '_blank'); } catch(e){}
            }

            if (data.details) addLog('ACTION', data.details);

            aiStatusTag.textContent = '✅ Online & Ready';
            aiStatusTag.style.color = 'var(--teal)';
            setBadge('সম্পন্ন ✓', '');

        } catch (err) {
            jarvisOutput.textContent = '❌ সার্ভারে অডিও পাঠানো যায়নি: ' + err.message;
            addLog('ERROR', err.message);
            setBadge('ত্রুটি ❌', 'active');
        } finally {
            isExecuting = false;
        }
    }

    // ────────────────────────────────────────────────────────
    // 💻 Mode 2: Hardware USB Mic (Python SoundDevice)
    // ────────────────────────────────────────────────────────
    async function startHardwareMic() {
        if (isExecuting) return;
        isExecuting = true;
        isListening = true;
        btnToggleMic.classList.add('active');
        pulseContainer.classList.add('listening');
        micStatusText.textContent = 'পিসি শুনছে... বলুন';
        liveSpeechText.textContent = '🎙️ পিসির USB মাইক্রোফোন সক্রিয় — কথা বলুন...';
        setBadge('পিসি মাইক সক্রিয়', 'active');
        startVisualizer();

        try {
            const res = await fetch('/api/listen_mic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lang: langSelect.value })
            });
            const data = await res.json();

            if (data.transcript) {
                liveSpeechText.textContent = '✅ ' + data.transcript;
                addLog('USER', `"${data.transcript}"`);
            } else {
                liveSpeechText.textContent = data.reply || 'কোনো কথা পাওয়া যায়নি।';
            }

            if (data.reply) {
                jarvisOutput.textContent = data.reply;
                playBengaliAudio(data.reply);
                addLog('JARVIS', data.reply);
            }

            if (data.details) addLog('ACTION', data.details);
            setBadge('সম্পন্ন ✓', '');

        } catch (err) {
            jarvisOutput.textContent = '❌ পিসি মাইক এরর: ' + err.message;
            addLog('ERROR', err.message);
        } finally {
            isExecuting = false;
            isListening = false;
            stopVisuals();
        }
    }

    // ────────────────────────────────────────────────────────
    // ⚡ Mode 3: Chrome Web Speech API
    // ────────────────────────────────────────────────────────
    if (SR) {
        recognition = new SR();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = langSelect.value;

        recognition.onstart = () => {
            isListening = true;
            btnToggleMic.classList.add('active');
            pulseContainer.classList.add('listening');
            micStatusText.textContent = 'শুনছি... এখন বলুন';
            liveSpeechText.textContent = '🎤 আপনার কথা শুনছি... বলুন';
            setBadge('মাইক সক্রিয়', 'active');
            startVisualizer();
        };

        recognition.onresult = (event) => {
            let t = '';
            for (let i = 0; i < event.results.length; i++) t += event.results[i][0].transcript;
            t = t.trim();
            if (!t) return;
            liveSpeechText.textContent = '✅ ' + t;
            clearTimeout(silenceTimer);
            silenceTimer = setTimeout(() => {
                if (t && !isExecuting) executeCommand(t);
            }, 500);
        };

        recognition.onerror = (e) => {
            console.warn('WebSpeech Error:', e.error);
            if (e.error === 'network') {
                addLog('NOTICE', 'ক্রোম লাইভ স্পিচ নেটওয়ার্ক সীমাবদ্ধতা — "ব্রাউজার রেকর্ডার" মোড ব্যবহার করুন');
                liveSpeechText.textContent = '💡 মোড পরিবর্তন করে "ব্রাউজার রেকর্ডার" সিলেক্ট করুন';
            }
        };

        recognition.onend = () => {
            if (isListening && micModeSelect.value === 'web_speech' && !isExecuting) {
                setTimeout(() => {
                    if (isListening) { try { recognition.start(); } catch(e){} }
                }, 200);
            } else if (!isListening) {
                stopVisuals();
            }
        };
    }

    // ── Mic Toggle Click ──
    btnToggleMic.addEventListener('click', () => {
        const mode = micModeSelect ? micModeSelect.value : 'media_recorder';

        if (mode === 'hardware_mic') {
            startHardwareMic();
        } else if (mode === 'web_speech') {
            if (!recognition) {
                alert('আপনার ব্রাউজারে Web Speech নেই। "ব্রাউজার রেকর্ডার" মোড ব্যবহার করুন।');
                return;
            }
            if (isListening) {
                isListening = false;
                try { recognition.stop(); } catch(e){}
                stopVisuals();
            } else {
                recognition.lang = langSelect.value;
                try { recognition.start(); } catch(e){}
            }
        } else {
            // Default: media_recorder
            if (isListening) {
                stopMediaRecording();
            } else {
                startMediaRecording();
            }
        }
    });

    // স্পেস বার চাপলে মাইক অন/অফ
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && document.activeElement !== manualInput) {
            e.preventDefault();
            btnToggleMic.click();
        }
    });

    // ── Force Run (⚡) ──
    btnForceRun && btnForceRun.addEventListener('click', () => {
        const mode = micModeSelect ? micModeSelect.value : 'media_recorder';
        if (mode === 'media_recorder' && isListening) {
            stopMediaRecording();
        }
    });

    function stopVisuals() {
        btnToggleMic.classList.remove('active');
        pulseContainer.classList.remove('listening');
        micStatusText.textContent = 'মাইক্রোফোন চালু করুন';
        setBadge('প্রস্তুত', '');
        stopVisualizer();
    }

    function setBadge(text, cls) {
        if (!speechBadge) return;
        speechBadge.textContent = text;
        speechBadge.className = 'state-badge ' + (cls || '');
    }

    // ────────────────────────────────────────────────────────
    // 🚀 Execute Command via Backend
    // ────────────────────────────────────────────────────────
    async function executeCommand(cmdText) {
        if (!cmdText || !cmdText.trim()) return;
        if (isExecuting) return;

        const clean = cmdText.trim();
        isExecuting = true;
        setBadge('⚡ এক্সিকিউট হচ্ছে...', 'executing');
        aiStatusTag.textContent = 'কাজ করছি...';
        aiStatusTag.style.color = '#ffb800';
        jarvisOutput.textContent = '⏳ কমান্ড পাঠানো হচ্ছে...';

        addLog('USER', `"${clean}"`);

        try {
            const res = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: clean, speak_pc: false })
            });
            const data = await res.json();

            const reply = data.reply || '';
            if (reply) {
                jarvisOutput.textContent = reply;
                playBengaliAudio(reply);
                addLog('JARVIS', reply);
            }

            if (data.details) addLog('ACTION', data.details);

            aiStatusTag.textContent = '✅ Online & Ready';
            aiStatusTag.style.color = 'var(--teal)';
            setBadge('সম্পন্ন ✓', '');
            liveSpeechText.textContent = '🎤 পরবর্তী কমান্ড বলুন...';

        } catch (err) {
            jarvisOutput.textContent = '❌ সার্ভার সংযোগ ব্যর্থ: ' + err.message;
            addLog('ERROR', err.message);
            setBadge('ত্রুটি ❌', 'active');
        } finally {
            isExecuting = false;
        }
    }

    // ── Bengali Audio Player ──
    let activeAudio = null;
    function playBengaliAudio(text) {
        if (!text) return;
        try {
            if (activeAudio) {
                activeAudio.pause();
                activeAudio = null;
            }
            activeAudio = new Audio('/api/tts?text=' + encodeURIComponent(text));
            activeAudio.volume = 1.0;
            activeAudio.play().catch(() => {});
        } catch(e) {}
    }

    // ── Text Input Form ──
    textForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const t = manualInput.value.trim();
        if (!t) return;
        liveSpeechText.textContent = '✅ ' + t;
        executeCommand(t);
        manualInput.value = '';
        manualInput.focus();
    });

    // ── Quick Chip Buttons ──
    document.querySelectorAll('.chip-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const cmd = btn.getAttribute('data-cmd');
            liveSpeechText.textContent = '✅ ' + cmd;
            executeCommand(cmd);
        });
    });

    // ── Clear Logs ──
    btnClearLogs.addEventListener('click', () => {
        logContainer.innerHTML = '';
        addLog('SYSTEM', 'লগ পরিষ্কার করা হয়েছে।');
    });

    function addLog(badge, text) {
        const t = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const el = document.createElement('div');
        el.className = 'log-item';
        el.innerHTML = `
            <span class="log-time">${t}</span>
            <span class="log-badge">${badge}</span>
            <span class="log-text">${escapeHtml(text)}</span>
        `;
        logContainer.prepend(el);
        while (logContainer.children.length > 50) logContainer.removeChild(logContainer.lastChild);
    }

    function escapeHtml(s) {
        const d = document.createElement('div');
        d.textContent = s;
        return d.innerHTML;
    }

    // ────────────────────────────────────────────────────────
    // 🌊 Dynamic Audio Waveform Visualizer
    // ────────────────────────────────────────────────────────
    let phase = 0;

    function startVisualizer() {
        if (animFrameId) cancelAnimationFrame(animFrameId);
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const cy = canvas.height / 2;

            let amp = 16;
            if (analyser) {
                const arr = new Uint8Array(analyser.frequencyBinCount);
                analyser.getByteFrequencyData(arr);
                let sum = 0;
                for (let i = 0; i < arr.length; i++) sum += arr[i];
                amp = Math.max(8, (sum / arr.length) * 0.8);
            }

            ctx.beginPath();
            ctx.strokeStyle = '#00f0ff';
            ctx.lineWidth = 2.5;
            for (let x = 0; x < canvas.width; x++) {
                const a = Math.sin(x * 0.05 + phase) * amp * Math.sin(x / canvas.width * Math.PI);
                x === 0 ? ctx.moveTo(x, cy + a) : ctx.lineTo(x, cy + a);
            }
            ctx.stroke();

            phase += 0.1;
            if (isListening) animFrameId = requestAnimationFrame(draw);
        }
        draw();
    }

    function stopVisualizer() {
        if (animFrameId) { cancelAnimationFrame(animFrameId); animFrameId = null; }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.strokeStyle = 'rgba(0,240,255,0.2)';
        ctx.lineWidth = 1;
        ctx.moveTo(0, canvas.height / 2);
        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
    }

    stopVisualizer();
    addLog('SYSTEM', 'JARVIS সিস্টেম সক্রিয়! মাইক্রোফোন বাটনে ক্লিক করে কথা বলুন।');
});
