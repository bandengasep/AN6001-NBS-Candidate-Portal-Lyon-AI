import { BookOpen, Users, Award, HelpCircle, Building } from 'lucide-react';

const quickQuestions = [
  {
    icon: BookOpen,
    label: 'MBA Programs',
    question: 'What MBA programmes does NBS offer?',
  },
  {
    icon: Users,
    label: 'MSc Options',
    question: 'What MSc programmes are available at NBS?',
  },
  {
    icon: Award,
    label: 'Requirements',
    question: 'What are the admission requirements for NBS programmes?',
  },
  {
    icon: HelpCircle,
    label: 'Compare Programs',
    question: 'Can you compare the MBA and MSc Business Analytics programmes?',
  },
  {
    icon: Building,
    label: 'About NBS',
    question: 'Tell me about NBS rankings and accreditations',
  },
];

export function Sidebar({ onQuestionClick }) {
  return (
    <aside className="w-64 bg-gray-50 border-r border-gray-200 p-4 hidden lg:block">
      <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wider mb-4">
        Quick Questions
      </h2>

      <div className="space-y-2">
        {quickQuestions.map((item, index) => (
          <button
            key={index}
            onClick={() => onQuestionClick(item.question)}
            className="w-full flex items-center space-x-3 p-3 rounded-lg text-left hover:bg-gray-100 transition-colors group"
          >
            <item.icon className="h-5 w-5 text-gray-400 group-hover:text-nbs-red transition-colors" />
            <span className="text-sm text-gray-700 group-hover:text-gray-900">
              {item.label}
            </span>
          </button>
        ))}
      </div>

      <hr className="my-6 border-gray-200" />

      <div className="text-xs text-gray-500 space-y-2">
        <p className="font-medium text-gray-600">About this Advisor</p>
        <p>
          This AI assistant provides information about NBS degree programmes.
          For official information, please visit the NBS website.
        </p>
        <p className="text-gray-400 mt-4">
          Powered by AI | Nanyang Business School
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
