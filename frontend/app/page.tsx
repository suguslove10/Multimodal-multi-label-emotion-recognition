'use client';

import { useState, useRef } from 'react';
import { Upload, Mic, Camera, Sparkles, Brain, TrendingUp } from 'lucide-react';

export default function Home() {
  const [text, setText] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [audio, setAudio] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isCameraOn, setIsCameraOn] = useState(false);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsCameraOn(true);
      }
    } catch (err) {
      alert('Camera access denied');
    }
  };

  const capturePhoto = () => {
    if (videoRef.current) {
      const canvas = document.createElement('canvas');
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx?.drawImage(videoRef.current, 0, 0);
      
      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
          setImage(file);
          setImagePreview(URL.createObjectURL(blob));
          stopCamera();
        }
      });
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      setIsCameraOn(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      const chunks: BlobPart[] = [];

      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        const file = new File([blob], 'recording.wav', { type: 'audio/wav' });
        setAudio(file);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      alert('Microphone access denied');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!text || !image || !audio) {
      alert('Please provide all three inputs');
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
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert('Error analyzing emotions. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-pink-500">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-4 flex items-center justify-center gap-3">
            <Sparkles className="w-12 h-12" />
            AI Emotion Recognition
          </h1>
          <p className="text-white/90 text-lg">
            Advanced multimodal emotion analysis using Deep Learning
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Input Panel */}
          <div className="bg-white rounded-2xl shadow-2xl p-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
              <Upload className="w-6 h-6" />
              Input Data
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Text Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  💭 How are you feeling?
                </label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Express your emotions in words..."
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
                  rows={3}
                />
              </div>

              {/* Image Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  📸 Facial Expression
                </label>
                <div className="space-y-3">
                  {!isCameraOn ? (
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={startCamera}
                        className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center gap-2"
                      >
                        <Camera className="w-4 h-4" />
                        Open Camera
                      </button>
                      <label className="flex-1 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors flex items-center justify-center gap-2 cursor-pointer">
                        <Upload className="w-4 h-4" />
                        Upload Photo
                        <input
                          type="file"
                          accept="image/*"
                          onChange={handleImageUpload}
                          className="hidden"
                        />
                      </label>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <video
                        ref={videoRef}
                        autoPlay
                        className="w-full rounded-lg"
                      />
                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={capturePhoto}
                          className="flex-1 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                        >
                          Capture
                        </button>
                        <button
                          type="button"
                          onClick={stopCamera}
                          className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}
                  {imagePreview && (
                    <img src={imagePreview} alt="Preview" className="w-full rounded-lg" />
                  )}
                </div>
              </div>

              {/* Audio Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  🎙️ Voice Recording
                </label>
                <button
                  type="button"
                  onClick={isRecording ? stopRecording : startRecording}
                  className={`w-full px-4 py-3 rounded-lg text-white font-semibold transition-all flex items-center justify-center gap-2 ${
                    isRecording
                      ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                      : 'bg-purple-500 hover:bg-purple-600'
                  }`}
                >
                  <Mic className="w-5 h-5" />
                  {isRecording ? 'Stop Recording' : audio ? 'Re-record' : 'Start Recording'}
                </button>
                {audio && !isRecording && (
                  <p className="text-sm text-green-600 mt-2">✓ Audio recorded</p>
                )}
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || !text || !image || !audio}
                className="w-full px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 flex items-center justify-center gap-2"
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
            </form>
          </div>

          {/* Results Panel */}
          <div className="bg-white rounded-2xl shadow-2xl p-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
              <TrendingUp className="w-6 h-6" />
              Analysis Results
            </h2>

            {!result ? (
              <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                <Brain className="w-16 h-16 mb-4" />
                <p className="text-lg">Awaiting analysis...</p>
                <p className="text-sm">Provide all inputs and click analyze</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Emotion Cards */}
                <div className="grid grid-cols-3 gap-3">
                  <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border-l-4 border-blue-500">
                    <p className="text-xs text-blue-600 font-semibold mb-1">TEXT</p>
                    <p className="text-xl font-bold text-gray-800">{result.text.label}</p>
                    <p className="text-sm text-gray-600">{(result.text.score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border-l-4 border-purple-500">
                    <p className="text-xs text-purple-600 font-semibold mb-1">IMAGE</p>
                    <p className="text-xl font-bold text-gray-800">{result.image.label}</p>
                    <p className="text-sm text-gray-600">{(result.image.score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="bg-gradient-to-br from-pink-50 to-pink-100 p-4 rounded-lg border-l-4 border-pink-500">
                    <p className="text-xs text-pink-600 font-semibold mb-1">AUDIO</p>
                    <p className="text-xl font-bold text-gray-800">{result.audio.label}</p>
                    <p className="text-sm text-gray-600">{(result.audio.score * 100).toFixed(1)}%</p>
                  </div>
                </div>

                {/* Chart */}
                {result.chart && (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <img
                      src={`data:image/png;base64,${result.chart}`}
                      alt="Confidence Chart"
                      className="w-full"
                    />
                  </div>
                )}

                {/* ML Predictions */}
                <div className="bg-gradient-to-r from-yellow-50 to-orange-50 p-4 rounded-lg border-2 border-yellow-300">
                  <h3 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                    <Brain className="w-5 h-5" />
                    Machine Learning Predictions
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Decision Tree</p>
                      <p className="text-2xl font-bold text-gray-800">{result.ml_predictions.decision_tree}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">K-Nearest Neighbors</p>
                      <p className="text-2xl font-bold text-gray-800">{result.ml_predictions.knn}</p>
                    </div>
                  </div>
                </div>

                {/* Stats */}
                <div className="text-center text-sm text-gray-600">
                  ✅ Analysis saved • Total records: {result.total_records}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
