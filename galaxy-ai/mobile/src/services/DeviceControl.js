/**
 * Galaxy AI Mobile - Android Device Control & Intent Launcher
 * Dispatches native intents to Android system (YouTube, Facebook, Alarms, etc.)
 */

import { Linking, Platform, Alert } from 'react-native';

class DeviceControlService {
  // Launch external Android application by scheme or package
  async launchApp(appName, fallbackUrl = '') {
    const name = appName.toLowerCase().trim();

    const intentMap = {
      youtube: {
        scheme: 'vnd.youtube://',
        web: 'https://youtube.com',
      },
      facebook: {
        scheme: 'fb://facewebmodal/f?href=https://facebook.com',
        web: 'https://facebook.com',
      },
      instagram: {
        scheme: 'instagram://app',
        web: 'https://instagram.com',
      },
      whatsapp: {
        scheme: 'whatsapp://send',
        web: 'https://web.whatsapp.com',
      },
      camera: {
        scheme: 'camera:',
        web: '',
      },
    };

    const target = intentMap[name];
    if (!target) {
      if (fallbackUrl) {
        return Linking.openURL(fallbackUrl);
      }
      return false;
    }

    try {
      const supported = await Linking.canOpenURL(target.scheme);
      if (supported) {
        await Linking.openURL(target.scheme);
        return { success: true, message: `Launched ${appName} natively.` };
      } else if (target.web) {
        await Linking.openURL(target.web);
        return { success: true, message: `Opened ${appName} via browser.` };
      }
    } catch (err) {
      console.warn(`[DeviceControl] Failed opening ${appName}:`, err);
      if (target.web) {
        await Linking.openURL(target.web);
      }
    }
  }

  // Set an Android Alarm
  async setAlarm(hour = 7, minutes = 0, message = 'Galaxy AI Morning Brief') {
    // Android clock alarm intent scheme
    const alarmUri = `intent:#Intent;action=android.intent.action.SET_ALARM;i.android.intent.extra.HOUR=${hour};i.android.intent.extra.MINUTES=${minutes};S.android.intent.extra.MESSAGE=${encodeURIComponent(
      message
    )};end`;

    try {
      if (Platform.OS === 'android') {
        await Linking.openURL(alarmUri);
        return { success: true, message: `Alarm set for ${hour}:${minutes}` };
      } else {
        return { success: true, message: `Simulated alarm for ${hour}:${minutes}` };
      }
    } catch (e) {
      return { success: false, message: 'Alarm intent failed on this device' };
    }
  }

  // Open Device Settings
  async openSettings() {
    try {
      await Linking.openSettings();
      return { success: true };
    } catch (e) {
      return { success: false, error: e.message };
    }
  }
}

export default new DeviceControlService();

