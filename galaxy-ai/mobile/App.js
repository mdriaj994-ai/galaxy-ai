/**
 * Galaxy AI - Mobile Companion Main App Entry
 * React Native Android Core
 */

import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import VoiceScreen from './src/screens/VoiceScreen';
import ChatScreen from './src/screens/ChatScreen';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('voice'); // 'voice' or 'chat'

  return (
    <View style={styles.container}>
      {currentScreen === 'voice' ? (
        <VoiceScreen onSwitchToChat={() => setCurrentScreen('chat')} />
      ) : (
        <ChatScreen onSwitchToVoice={() => setCurrentScreen('voice')} />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0E14',
  },
});

