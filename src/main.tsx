import { Devvit } from '@devvit/public-api';
import { haeHuumorivideot } from './index.js';

Devvit.configure({
  redditAPI: true,
});

// Luodaan Devvit-sovelluksen käyttöliittymä
Devvit.addCustomPostType({
  name: 'Reddit Huumorivideot',
  height: 'tall',
  render: (context) => {
    // Haetaan videot komponentin latautuessa
    const [videot] = Devvit.useState(async () => {
      return await haeHuumorivideot();
    });

    if (!videot || videot.length === 0) {
      return (
        <vstack padding="medium" gap="medium" alignment="center middle">
          <text size="large">Haetaan huumorivideoita Redditistä...</text>
        </vstack>
      );
    }

    return (
      <vstack padding="medium" gap="medium">
        <text size="xlarge" weight="bold">😂 Redditin Parhaat Viraalivideot</text>
        {videot.slice(0, 3).map((v, index) => (
          <vstack key={index} backgroundColor="neutral-background-weak" padding="small" cornerRadius="medium" gap="small">
            <text weight="bold">{v.title}</text>
            <text size="small">💬 Ääniä: {v.score}</text>
            <url target={v.permalink}>Katso tai kommentoi Redditissä</url>
          </vstack>
        ))}
      </vstack>
    );
  },
});

export default Devvit;
