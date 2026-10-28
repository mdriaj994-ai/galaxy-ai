/**
 * Galaxy AI Mobile - Android Voice Screen
 * Voice listening orb & automatic intent dispatcher.
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  ScrollView,
} from 'react-native';
import DeviceControl from '../services/DeviceControl';

export default function VoiceScreen({ onSwitchToChat }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [statusMessage, setStatusMessage] = useState('Tap the core to speak.');

  const toggleVoice = () => {
    if (isListening) {
      setIsListening(false);
      setStatusMessage('Voice capture stopped.');
    } else {
      setIsListening(true);
      setStatusMessage('Listening to voice frequency...');
      setTranscript('');

      // Simulate voice capture
      setTimeout(() => {
        const sampleVoiceCommands = [
          'Open YouTube and play quantum physics lecture',
          'Set alarm for 7 AM morning schedule',
          'Launch Facebook and check messages',
          'Open camera to document blueprint',
        ];
        const chosen = sampleVoiceCommands[Math.floor(Math.random() * sampleVoiceCommands.length)];
        setTranscript(chosen);
        handleExecute(chosen);
      }, 2200);
    }
  };

  const handleExecute = async (command) => {
    setIsListening(false);
    const low = command.toLowerCase();

    if (low.includes('youtube')) {
      setStatusMessage('Launching YouTube Android Intent...');
      await DeviceControl.launchApp('youtube');
    } else if (low.includes('alarm')) {
      setStatusMessage('Setting Device Alarm for 07:00 AM...');
      await DeviceControl.setAlarm(7, 0, 'Galaxy AI Schedule');
    } else if (low.includes('facebook') || low.includes('fb')) {
      setStatusMessage('Launching Facebook Android Intent...');
      await DeviceControl.launchApp('facebook');
    } else if (low.includes('camera')) {
      setStatusMessage('Opening Camera Viewfinder...');
      await DeviceControl.launchApp('camera');
    } else {
      setStatusMessage(`Processed instruction: "${command}"`);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0B0E14" />

      {/* Top Bar */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>GALAXY AI</Text>
          <Text style={styles.subtitle}>Mobile Operating Core</Text>
        </View>
        <TouchableOpacity style={styles.chatButton} onPress={onSwitchToChat}>
          <Text style={styles.chatButtonText}>Chat & Files</Text>
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {/* Animated Central Orb */}
        <View style={styles.orbWrapper}>
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={toggleVoice}
            style={[
              styles.orb,
              isListening ? styles.orbListening : styles.orbIdle,
            ]}
          >
            <View style={styles.orbInner}>
              <Text style={styles.orbText}>{isListening ? 'LISTENING' : 'ACTIVATE'}</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* Live Transcript Display */}
        <View style={styles.transcriptBox}>
          <Text style={styles.boxLabel}>VOICE STREAM TRANSCRIPTION</Text>
          <Text style={styles.transcriptText}>
            {transcript || 'No voice detected. Tap Activate to speak.'}
          </Text>
        </View>

        {/* Status Feedback */}
        <View style={styles.statusBox}>
          <Text style={styles.statusLabel}>DEVICE INTENT TELEMETRY</Text>
          <Text style={styles.statusText}>{statusMessage}</Text>
        </View>

        {/* Quick Action Chips */}
        <Text style={styles.chipsTitle}>QUICK INTENTS</Text>
        <View style={styles.chipsRow}>
          {['Open YouTube', 'Set 7 AM Alarm', 'Open Facebook', 'Launch Camera'].map((chip) => (
            <TouchableOpacity
              key={chip}
              style={styles.chip}
              onPress={() => {
                setTranscript(chip);
                handleExecute(chip);
              }}
            >
              <Text style={styles.chipText}>{chip}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0E14',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#161D2B',
  },
  title: {
    color: '#00F0FF',
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 1.5,
  },
  subtitle: {
    color: '#94A3B8',
    fontSize: 10,
    fontFamily: Platform.OS === 'android' ? 'monospace' : 'Courier',
  },
  chatButton: {
    backgroundColor: '#161D2B',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#7000FF',
  },
  chatButtonText: {
    color: '#E2E8F0',
    fontSize: 12,
    fontWeight: '600',
  },
  content: {
    padding: 20,
    alignItems: 'center',
  },
  orbWrapper: {
    marginVertical: 30,
    alignItems: 'center',
    justifyContent: 'center',
  },
  orb: {
    width: 170,
    height: 170,
    borderRadius: 85,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
  },
  orbIdle: {
    borderColor: '#00F0FF',
    backgroundColor: 'rgba(0, 240, 255, 0.05)',
  },
  orbListening: {
    borderColor: '#7000FF',
    backgroundColor: 'rgba(112, 0, 255, 0.2)',
  },
  orbInner: {
    width: 130,
    height: 130,
    borderRadius: 65,
    backgroundColor: '#121722',
    justifyContent: 'center',
    alignItems: 'center',
  },
  orbText: {
    color: '#00F0FF',
    fontSize: 11,
    fontWeight: 'bold',
    letterSpacing: 2,
  },
  transcriptBox: {
    width: '100%',
    backgroundColor: '#161D2B',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    borderColor: '#1E293B',
    marginBottom: 12,
  },
  boxLabel: {
    color: '#64748B',
    fontSize: 9,
    fontFamily: Platform.OS === 'android' ? 'monospace' : 'Courier',
    marginBottom: 6,
  },
  transcriptText: {
    color: '#E2E8F0',
    fontSize: 13,
  },
  statusBox: {
    width: '100%',
    backgroundColor: '#121722',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    borderColor: '#7000FF',
    marginBottom: 20,
  },
  statusLabel: {
    color: '#7000FF',
    fontSize: 9,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  statusText: {
    color: '#00F0FF',
    fontSize: 12,
  },
  chipsTitle: {
    color: '#64748B',
    fontSize: 10,
    fontWeight: 'bold',
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  chipsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    width: '100%',
  },
  chip: {
    backgroundColor: '#161D2B',
    borderWidth: 1,
    borderColor: '#334155',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 10,
  },
  chipText: {
    color: '#E2E8F0',
    fontSize: 11,
  },
});

