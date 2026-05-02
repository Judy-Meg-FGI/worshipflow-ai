# 🎵 WorshipFlow AI

**AI-Powered Worship Planning for Modern Churches**

WorshipFlow AI is a Streamlit web application that helps worship leaders generate structured praise and worship plans based on service themes. Whether you have access to OpenAI's GPT-4 or need a reliable fallback system, WorshipFlow AI delivers thoughtful, well-organized worship sets in seconds.

## ✨ Features

- **Theme-Based Planning**: Generate worship sets that align with your service theme
- **Flexible Inputs**: Customize service type, worship style, familiarity preferences, and durations
- **Smart Song Selection**: Avoid recently used songs and match congregation familiarity levels
- **Complete Output**:
  - 🎉 **Praise Medley**: 17-20 minute continuous medley with 4-6 songs
  - 🙏 **Worship Set**: 2-3 songs for deeper worship (~10 minutes)
  - 📖 **Theme Alignment**: Explanation of how songs connect to your theme
  - 🔄 **Transition Notes**: Practical ideas for smooth flow between songs
  - ✨ **New Song Suggestions**: Fresh songs to introduce to your congregation
  - 🎵 **Rehearsal Notes**: Key preparation areas for your team
- **AI or Fallback Mode**: Uses OpenAI GPT-4 when available, with intelligent fallback
- **Professional UI**: Clean, modern interface designed for ministry use

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd path/to/worshipflow_ai
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run worshipflow_ai.py
   ```

6. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Or manually navigate to that address

## 🔑 Optional: OpenAI Integration

For AI-generated worship plans, you can connect OpenAI's GPT-4:

1. **Get an OpenAI API key** from [OpenAI](https://platform.openai.com/api-keys)

2. **Set the environment variable**:
   ```bash
   # Windows (Command Prompt)
   set OPENAI_API_KEY=your_api_key_here

   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your_api_key_here"

   # macOS/Linux
   export OPENAI_API_KEY="your_api_key_here"
   ```

3. **Or create a `.env` file** in the project directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

**Note**: The app works perfectly in demo mode without an API key, using an intelligent fallback system with a comprehensive song database.

## 📖 How to Use

1. **Enter Service Details** in the sidebar:
   - **Service Theme**: The main theme or topic (e.g., "Grace", "Redemption", "Healing")
   - **Service Type**: Sunday Morning, Wednesday Night, Special Event, etc.
   - **Segment Type**: Full Service, Opening Praise & Worship, etc.
   - **Worship Style**: Contemporary, Traditional Hymns, Blended, Gospel, etc.
   - **Familiarity Preference**: Well-known favorites, Mix, or Mostly new songs
   - **Recently Used Songs**: Comma-separated list to avoid repetition
   - **Duration Settings**: Customize praise and worship segment lengths

2. **Click "Generate Worship Plan"** to create your customized worship set

3. **Review the Output**:
   - Song selections with keys, tempos, and durations
   - Theme alignment explanations
   - Transition ideas for smooth flow
   - New song suggestions
   - Rehearsal preparation notes

4. **Use the Export Options** to copy or download your plan

## 🎯 Example Use Cases

### Sunday Morning Service
- **Theme**: "God's Unfailing Love"
- **Style**: Contemporary
- **Familiarity**: Mix of familiar and new
- **Result**: A balanced set connecting songs about God's love with practical application

### Easter Service
- **Theme**: "He Is Risen"
- **Style**: Blended
- **Familiarity**: Well-known favorites
- **Result**: Celebratory praise medley leading into worship focused on resurrection

### Youth Service
- **Theme**: "Identity in Christ"
- **Style**: Contemporary
- **Familiarity**: Mostly new songs
- **Result**: Fresh, engaging songs that speak to young people's search for identity

### Healing Service
- **Theme**: "Divine Healing"
- **Style**: Charismatic
- **Familiarity**: Mix of familiar and new
- **Result**: Songs that create atmosphere for prayer and ministry

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web framework
- **AI Integration**: OpenAI GPT-4 (optional)
- **Fallback System**: Intelligent algorithm with 50+ song database
- **Styling**: Custom CSS for professional ministry aesthetic

### Song Database
The fallback system includes:
- 30+ praise songs (upbeat, mid-tempo options)
- 20+ worship songs (slower, contemplative)
- Theme-specific suggestions for common topics
- New song recommendations from current artists

### Filtering Logic
- Familiarity levels (High, Medium, Low)
- Tempo sorting for optimal flow
- Key compatibility considerations
- Recent song exclusion

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs or suggest features
- Submit song suggestions for the database
- Improve the UI/UX
- Add new theme categories

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- All songwriters and artists whose music is referenced in the database
- The worship leader community for inspiration and feedback
- Streamlit team for the excellent web app framework
- OpenAI for making AI accessible to ministry contexts

## 📞 Support

For questions, suggestions, or support:
- Open an issue on GitHub
- Email: support@worshipflow.ai (example)

## 🌟 Scripture

> "Sing to the Lord a new song; sing to the Lord, all the earth." - Psalm 96:1

> "Let the message of Christ dwell among you richly as you teach and admonish one another with all wisdom through psalms, hymns, and songs from the Spirit, singing to God with gratitude in your hearts." - Colossians 3:16

---

**Built with ❤️ for worship leaders everywhere**

*WorshipFlow AI v1.0*