import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const AXIS_LABELS = [
  'Quantitative',
  'Experience',
  'Leadership',
  'Tech & Analytics',
  'Business Domain',
  'Career Ambition',
  'Study Flexibility',
];

const AXIS_KEYS = [
  'quantitative',
  'experience',
  'leadership',
  'tech_analytics',
  'business_domain',
  'career_ambition',
  'study_flexibility',
];

/**
 * Spider/Radar chart for user profile and programme comparison.
 *
 * @param {Object} props
 * @param {Object} props.userScores - {quantitative: 1-5, ...} (partial OK, unfilled axes show 0)
 * @param {Array} props.programmeOverlays - [{name, scores: {quantitative: 1-5, ...}}]
 */
export function SpiderChart({ userScores = {}, programmeOverlays = [] }) {
  const userData = AXIS_KEYS.map(k => userScores[k] || 0);

  const datasets = [
    {
      label: 'Your Profile',
      data: userData,
      backgroundColor: 'rgba(224, 25, 50, 0.15)',
      borderColor: '#E01932',
      borderWidth: 2,
      pointBackgroundColor: '#E01932',
      pointRadius: 4,
    },
    ...programmeOverlays.map((prog, i) => {
      const colors = ['#0071BC', '#F79320', '#2D2D2D'];
      const color = colors[i % colors.length];
      return {
        label: prog.name,
        data: AXIS_KEYS.map(k => prog.scores[k] || 0),
        backgroundColor: `${color}15`,
        borderColor: color,
        borderWidth: 2,
        pointBackgroundColor: color,
        pointRadius: 3,
        borderDash: [4, 4],
      };
    }),
  ];

  const data = { labels: AXIS_LABELS, datasets };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      r: {
        min: 0,
        max: 5,
        ticks: {
          stepSize: 1,
          font: { size: 11 },
          backdropColor: 'transparent',
        },
        pointLabels: {
          font: { size: 12, weight: '500' },
          color: '#4A4A4A',
        },
        grid: { color: '#E5E5E5' },
        angleLines: { color: '#E5E5E5' },
      },
    },
    plugins: {
      legend: {
        position: 'bottom',
        labels: { font: { size: 12 }, usePointStyle: true, padding: 16 },
      },
    },
  };

  return <Radar data={data} options={options} />;
}
