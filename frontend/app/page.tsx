'use client';

import { useState, useRef, useEffect } from 'react';
import { Upload, Mic, Camera, Sparkles, Brain, TrendingUp, X, Check, AlertCircle } from 'lucide-react';

export default function Home() {
  const [text, setText] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [audio, setAudio] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [cameraLoading, setCameraLoading] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);

  const startCamera = async () => {
    setError('');
    setCameraLoading(true);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: true,
        audio: false
      });
      
      streamRef.current = stream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        
        // Simple approach - just set state after a short delay
        setTimeout(() => {
          setCameraLoading(false);
          setIsCameraOn(true);
        }, 500);
      }
    } catch (err: any) {
      console.error('Camera error:', err);
      setError('Camera access denied. Please allow camera permissions.');
      setCameraLoading(false);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(videoRef.current, 0, 0);
      
      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
          setImage(file);
          setImagePreview(canvas.toDataURL('image/jpeg'));
          stopCamera();
        }
      }, 'image/jpeg', 0.95);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraOn(false);
  };

  const startRecording = async () => {
    setError('');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const audioFile = new File([audioBlob], 'recording.webm', { type: 'audio/webm' });
        setAudio(audioFile);
        stream.getTracks().forEach(track => track.stop());
        setRecordingTime(0);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err: any) {
      console.error('Microphone error:', err);
      setError('Microphone access denied. Please allow microphone permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!text.trim()) {
      setError('Please enter your feelings in the text box');
      return;
    }
    
    if (!image) {
      setError('Please capture or upload a photo');
      return;
    }
    
    if (!audio) {
      setError('Please record audio');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('text', text);
    formData.append('image', image);
    formData.append('audio', audio);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Analysis failed');
      }
      
      const data = await response.json();
      setResult(data);
      setError('');
    } catch (error: any) {
      console.error('Error:', error);
      setError('Error analyzing emotions. Make sure the backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const resetAll = () => {
    setText('');
    setImage(null);
    setAudio(null);
    setImagePreview('');
    setResult(null);
    setError('');
    stopCamera();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-pink-500 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6 pt-4">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 flex items-center justify-center gap-3">
            <Sparkles className="w-10 h-10 md:w-12 md:h-12" />
            AI Emotion Recognition
          </h1>
          <p className="text-white/90 text-base md:text-lg">
            Multimodal emotion analysis using Deep Learning
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 bg-red-100 border-2 border-red-500 text-red-800 px-4 py-3 rounded-xl flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            <span className="font-semibold">{error}</span>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-4 max-w-full">
          {/* Input Panel */}
          <div className="bg-white rounded-2xl shadow-xl p-4 md:p-5 overflow-hidden">
            <h2 className="text-lg md:text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
              <Upload className="w-5 h-5 md:w-6 md:h-6" />
              Input Data
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Text Input */}
              <div>
                <label className="block text-sm font-bold text-gray-800 mb-2">
                  💭 How are you feeling?
                </label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="I feel happy because..."
                  className="w-full px-3 py-2 text-gray-900 bg-white border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all outline-none resize-none"
                  rows={3}
                  style={{ color: '#111827', backgroundColor: '#ffffff' }}
                />
              </div>

              {/* Image Input */}
              <div>
                <label className="block text-sm font-bold text-gray-800 mb-2">
                  📸 Facial Expression
                </label>
                
                {!isCameraOn && !imagePreview && !cameraLoading && (
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      onClick={startCamera}
                      className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all font-semibold text-sm flex items-center justify-center gap-2"
                    >
                      <Camera className="w-4 h-4" />
                      Camera
                    </button>
                    <label className="px-3 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-800 transition-all font-semibold text-sm flex items-center justify-center gap-2 cursor-pointer">
                      <Upload className="w-4 h-4" />
                      Upload
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                      />
                    </label>
                  </div>
                )}
                
                {cameraLoading && (
                  <div className="bg-gray-900 rounded-lg p-8 text-center">
                    <Camera className="w-12 h-12 mx-auto mb-3 text-white animate-pulse" />
                    <p className="text-white font-semibold">Starting camera...</p>
                    <p className="text-gray-400 text-sm mt-1">Please allow camera access</p>
                  </div>
                )}
                
                {isCameraOn && (
                  <div className="space-y-2">
                    <div className="relative bg-black rounded-lg overflow-hidden">
                      <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="w-full h-auto"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        type="button"
                        onClick={capturePhoto}
                        className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all font-bold text-sm flex items-center justify-center gap-2"
                      >
                        <Check className="w-4 h-4" />
                        Capture Photo
                      </button>
                      <button
                        type="button"
                        onClick={stopCamera}
                        className="px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all font-bold text-sm flex items-center justify-center gap-2"
                      >
                        <X className="w-4 h-4" />
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
                
                {imagePreview && !isCameraOn && (
                  <div className="relative">
                    <div className="relative w-full rounded-lg border-4 border-green-500 bg-gray-100 overflow-hidden">
                      <img 
                        src={imagePreview} 
                        alt="Preview" 
                        className="w-full h-auto max-h-64 object-contain mx-auto" 
                      />
                    </div>
                    <div className="absolute top-2 right-2 bg-green-600 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 shadow-lg">
                      <Check className="w-3 h-3" />
                      Ready
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        setImage(null);
                        setImagePreview('');
                      }}
                      className="absolute top-2 left-2 bg-red-600 text-white p-1.5 rounded-full hover:bg-red-700 transition-all shadow-lg"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </div>
                )}
              </div>

              {/* Audio Input */}
              <div>
                <label className="block text-sm font-bold text-gray-800 mb-2">
                  🎙️ Voice Recording
                </label>
                <button
                  type="button"
                  onClick={isRecording ? stopRecording : startRecording}
                  className={`w-full px-4 py-3 rounded-lg text-white font-bold transition-all flex items-center justify-center gap-2 text-sm ${
                    isRecording
                      ? 'bg-red-600 hover:bg-red-700 animate-pulse'
                      : audio
                      ? 'bg-green-600 hover:bg-green-700'
                      : 'bg-purple-600 hover:bg-purple-700'
                  }`}
                >
                  <Mic className="w-5 h-5" />
                  {isRecording ? (
                    <>Stop ({formatTime(recordingTime)})</>
                  ) : audio ? (
                    <>✓ Recorded</>
                  ) : (
                    <>Start Recording</>
                  )}
                </button>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full px-6 py-4 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 text-white font-bold rounded-lg hover:from-purple-700 hover:via-pink-700 hover:to-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 shadow-lg"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Analyze Emotions
                  </>
                )}
              </button>

              {result && (
                <button
                  type="button"
                  onClick={resetAll}
                  className="w-full px-4 py-2 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-all text-sm"
                >
                  Reset & Analyze Again
                </button>
              )}
            </form>
          </div>

          {/* Results Panel */}
          <div className="bg-white rounded-2xl shadow-xl p-4 md:p-5 overflow-hidden">
            <h2 className="text-lg md:text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 md:w-6 md:h-6" />
              Results
            </h2>

            {!result ? (
              <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                <Brain className="w-16 h-16 mb-3 opacity-50" />
                <p className="text-lg font-semibold">Awaiting analysis...</p>
                <p className="text-sm mt-1">Fill all inputs above</p>
              </div>
            ) : (
              <div className="space-y-4">
                {/* Emotion Cards */}
                <div className="grid grid-cols-3 gap-2">
                  <div className="bg-gradient-to-br from-blue-100 to-blue-200 p-3 rounded-lg border-l-4 border-blue-600">
                    <p className="text-xs text-blue-700 font-bold">TEXT</p>
                    <p className="text-lg font-bold text-gray-900">{result.text.label}</p>
                    <p className="text-xs text-gray-700 font-semibold">{(result.text.score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-100 to-purple-200 p-3 rounded-lg border-l-4 border-purple-600">
                    <p className="text-xs text-purple-700 font-bold">IMAGE</p>
                    <p className="text-lg font-bold text-gray-900">{result.image.label}</p>
                    <p className="text-xs text-gray-700 font-semibold">{(result.image.score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="bg-gradient-to-br from-pink-100 to-pink-200 p-3 rounded-lg border-l-4 border-pink-600">
                    <p className="text-xs text-pink-700 font-bold">AUDIO</p>
                    <p className="text-lg font-bold text-gray-900">{result.audio.label}</p>
                    <p className="text-xs text-gray-700 font-semibold">{(result.audio.score * 100).toFixed(1)}%</p>
                  </div>
                </div>

                {/* Chart */}
                {result.chart && (
                  <div className="bg-gray-50 p-3 rounded-lg overflow-hidden">
                    <img
                      src={`data:image/png;base64,${result.chart}`}
                      alt="Chart"
                      className="w-full h-auto rounded"
                    />
                  </div>
                )}

                {/* ML Predictions */}
                <div className="bg-gradient-to-r from-yellow-100 to-orange-100 p-4 rounded-lg border-2 border-yellow-400">
                  <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                    <Brain className="w-5 h-5" />
                    ML Predictions
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white p-2 rounded">
                      <p className="text-xs text-gray-600 font-semibold">Decision Tree</p>
                      <p className="text-xl font-bold text-gray-900">{result.ml_predictions.decision_tree}</p>
                    </div>
                    <div className="bg-white p-2 rounded">
                      <p className="text-xs text-gray-600 font-semibold">KNN</p>
                      <p className="text-xl font-bold text-gray-900">{result.ml_predictions.knn}</p>
                    </div>
                  </div>
                </div>

                {/* Stats */}
                <div className="text-center bg-green-100 text-green-800 py-2 px-3 rounded-lg font-semibold text-sm">
                  ✅ Saved • Total: {result.total_records}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
