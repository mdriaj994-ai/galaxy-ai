/**
 * Galaxy AI Mobile - Chat & File Analyzer Screen
 * Document parser (PDF/Images) and conversational automation.
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  SafeAreaView,
  Platform,
} from 'react-native';

export default function ChatScreen({ onSwitchToVoice }) {
  const [messages, setMessages] = useState([
    {
      id: '1',
      sender: 'ai',
      text: 'Mobile file analysis engine ready. Send prompts or attach documents for local parsing.',
      time: '12:00 PM',
    },
  ]);
  const [input, setInput] = useState('');

  const sendMessage = (customText = null) => {
    const text = customText || input;
    if (!text.trim()) return;

    const userMsg = {
      id: String(Date.now()),
      sender: 'user',
      text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [userMsg, ...prev]);
    if (!customText) setInput('');

    setTimeout(() => {
      const aiReply = {
        id: String(Date.now() + 1),
        sender: 'ai',
        text: `Mobile Core processed: "${text}". Local SQLite sync verified.`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [aiReply, ...prev]);
    }, 700);
  };

  const handleSimulateFile = (fileType) => {
    const name = fileType === 'pdf' ? 'Report_2026.pdf' : 'Blueprint_Scan.png';
    const userMsg = {
      id: String(Date.now()),
      sender: 'user',
      text: `[Attached ${name}]`,
      file: { name, type: fileType },
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [userMsg, ...prev]);

    setTimeout(() => {
      const replyMsg = {
        id: String(Date.now() + 1),
        sender: 'ai',
        text: `Analysis of ${name} complete: Verified 100% local syntax, 0 security vulnerabilities, local SQLite sync confirmed.`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [replyMsg, ...prev]);
    }, 1200);
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={onSwitchToVoice}>
          <Text style={styles.backButtonText}>← Voice Core</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>DOCUMENT ANALYZER</Text>
        <View style={{ width: 60 }} />
      </View>

      {/* Messages */}
      <FlatList
        inverted
        data={messages}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => (
          <View
            style={[
              styles.bubbleWrapper,
              item.sender === 'user' ? styles.bubbleUserWrapper : styles.bubbleAiWrapper,
            ]}
          >
            <View
              style={[
                styles.bubble,
                item.sender === 'user' ? styles.bubbleUser : styles.bubbleAi,
              ]}
            >
              {item.file && (
                <View style={styles.fileCard}>
                  <Text style={styles.fileCardText}>📄 {item.file.name}</Text>
                </View>
              )}
              <Text
                style={[
                  styles.messageText,
                  item.sender === 'user' ? styles.messageTextUser : styles.messageTextAi,
                ]}
              >
                {item.text}
              </Text>
            </View>
            <Text style={styles.timestamp}>{item.time}</Text>
          </View>
        )}
      />

      {/* Quick Attachments Bar */}
      <View style={styles.attachRow}>
        <TouchableOpacity
          style={styles.attachBtn}
          onPress={() => handleSimulateFile('pdf')}
        >
          <Text style={styles.attachBtnText}>+ PDF Upload</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.attachBtn}
          onPress={() => handleSimulateFile('image')}
        >
          <Text style={styles.attachBtnText}>+ Image Scan</Text>
        </TouchableOpacity>
      </View>

      {/* Input */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Ask Galaxy Mobile..."
          placeholderTextColor="#64748B"
        />
        <TouchableOpacity style={styles.sendButton} onPress={() => sendMessage()}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
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
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#161D2B',
  },
  headerTitle: {
    color: '#00F0FF',
    fontSize: 13,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  backButton: {
    paddingVertical: 4,
    paddingHorizontal: 8,
  },
  backButtonText: {
    color: '#94A3B8',
    fontSize: 12,
  },
  listContent: {
    padding: 16,
  },
  bubbleWrapper: {
    marginBottom: 12,
  },
  bubbleUserWrapper: {
    alignItems: 'flex-end',
  },
  bubbleAiWrapper: {
    alignItems: 'flex-start',
  },
  bubble: {
    maxWidth: '85%',
    padding: 12,
    borderRadius: 16,
  },
  bubbleUser: {
    backgroundColor: '#00F0FF',
    borderTopRightRadius: 2,
  },
  bubbleAi: {
    backgroundColor: '#161D2B',
    borderTopLeftRadius: 2,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  fileCard: {
    backgroundColor: 'rgba(0,0,0,0.2)',
    padding: 6,
    borderRadius: 6,
    marginBottom: 6,
  },
  fileCardText: {
    color: '#E2E8F0',
    fontSize: 11,
    fontWeight: 'bold',
  },
  messageText: {
    fontSize: 12,
    lineHeight: 18,
  },
  messageTextUser: {
    color: '#0B0E14',
    fontWeight: '600',
  },
  messageTextAi: {
    color: '#E2E8F0',
  },
  timestamp: {
    color: '#475569',
    fontSize: 9,
    marginTop: 3,
    paddingHorizontal: 4,
  },
  attachRow: {
    flexDirection: 'row',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: '#161D2B',
  },
  attachBtn: {
    backgroundColor: '#121722',
    borderWidth: 1,
    borderColor: '#334155',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  attachBtnText: {
    color: '#00F0FF',
    fontSize: 10,
    fontWeight: 'bold',
  },
  inputContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingBottom: 16,
    paddingTop: 8,
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: '#161D2B',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 10,
    color: '#E2E8F0',
    fontSize: 12,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  sendButton: {
    backgroundColor: '#7000FF',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  sendButtonText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: 'bold',
  },
});

