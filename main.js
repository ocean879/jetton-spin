const fs = require('fs');
const axios = require('axios');
const chalk = require('chalk');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const secureHeaders = fs.readFileSync('query.txt', 'utf8')
  .split('\n')
  .filter(line => line.trim().startsWith('query_id='));

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const getTime = () => {
  const now = new Date();
  return chalk.cyan(`[${now.toLocaleTimeString('id-ID', { hour12: false })}]`);
};

const spin = async (secureHeader, index, totalSpin) => {
  let count = 0;
  for (let i = 0; i < totalSpin; i++) {
    try {
      const response = await axios.post(
        'https://api.jtmkbot.click/roulette/spin',
        {},
        {
          headers: {
            'secure-header': secureHeader,
            'origin': 'https://v2.jtmkbot.click',
            'referer': 'https://v2.jtmkbot.click/',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/135.0.0.0 Safari/537.36'
          }
        }
      );

      const prize = response.data.secondLine.prize;
      count++;

      if (!prize) {
        console.log(`${getTime()} ${chalk.red(`🔴 [Akun ${index + 1}] Spin ke-${count}: ZONK`)}`);
      } else {
        const amount = prize.tickets;
        console.log(`${getTime()} ${chalk.green(`🟢 [Akun ${index + 1}] Spin ke-${count}: Dapat reward ${amount} Coins`)}`);
      }
    } catch (err) {
      if (err.response?.data?.message?.includes('next spin in')) {
        console.log(`${getTime()} ${chalk.yellow(`⚠️ [Akun ${index + 1}] Spin dihentikan karena sudah mencapai batas harian.`)}`);
        break;
      } else {
        console.log(`${getTime()} ${chalk.red(`❌ [Akun ${index + 1}] Gagal Spin: ${err.message}`)}`);
      }
    }
    await delay(5000);
  }
};

const dailyClaim = async (secureHeader, index) => {
  try {
    await axios.post('https://api.jtmkbot.click/daily_reward/claim', {}, {
      headers: {
        'secure-header': secureHeader,
        'origin': 'https://v2.jtmkbot.click',
        'referer': 'https://v2.jtmkbot.click/',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/135.0.0.0 Safari/537.36'
      }
    });
    console.log(`${getTime()} ${chalk.yellow(`✅ [Akun ${index + 1}] Daily reward berhasil diklaim`)}`);
  } catch {
    console.log(`${getTime()} ${chalk.red(`📦 [Akun ${index + 1}] Daily reward sudah diklaim hari ini`)}`);
  }
};

const buyLootBox = async (secureHeader, index) => {
  try {
    const res = await axios.post('https://api.jtmkbot.click/loot_box/purchase', {}, {
      headers: {
        'secure-header': secureHeader,
        'origin': 'https://v2.jtmkbot.click',
        'referer': 'https://v2.jtmkbot.click/',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/135.0.0.0 Safari/537.36'
      }
    });

    const reward = res.data.message;
    let output = '';

    if (reward.includes('Energi')) {
      output = chalk.hex('#FFA500')(`⚡ ${reward}`);
    } else if (reward.includes('100 Coins') || reward.includes('200 Coins')) {
      output = chalk.yellow(`🪙 ${reward}`);
    } else if (reward.includes('Crystal')) {
      output = chalk.cyanBright(`💎 ${reward}`);
    } else if (reward.match(/\$\d+/)) {
      output = chalk.green(`💰 ${reward}`);
    } else {
      output = reward;
    }

    console.log(`${getTime()} ${chalk.yellow(`🎁 [Akun ${index + 1}] Dapat Loot Box: ${output}`)}`);
  } catch {
    console.log(`${getTime()} ${chalk.red(`📦 [Akun ${index + 1}] Loot box sudah diklaim hari ini`)}`);
  }
};

rl.question(`${getTime()} ${chalk.cyanBright('Silakan input mau berapa spin: ')} `, async (answer) => {
  const totalSpin = parseInt(answer);
  rl.close();

  for (let i = 0; i < secureHeaders.length; i++) {
    const secureHeader = secureHeaders[i];
    await dailyClaim(secureHeader, i);
    await spin(secureHeader, i, totalSpin);
    await buyLootBox(secureHeader, i);
    console.log(`${getTime()} ${chalk.green(`✅ [Akun ${i + 1}] Selesai ${totalSpin} spin`)}`);
  }
});
