# Mining Incremental [![itch.io](https://img.shields.io/badge/Available_on-itch.io-FA5C5C?logo=itchdotio)](https://roxicaro.itch.io/mining-incremental) [![GPL-3.0 License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE) ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/roxicaro/Mining_Incremental) 

Basic terminal-based Incremental game project with ascii art-style. 
- **Report bugs**: [GitHub Issues](https://github.com/Roxicaro/Mining_Incremental/issues)  
- **Suggest features**: Comment on [itch.io](https://roxicaro.itch.io/mining-incremental)  <br>
<a href="https://roxicaro.itch.io/mining-incremental">
  <img src="https://static.itch.io/images/badge.svg" alt="Play on itch.io" width="200">
</a>  
<br>
<img src = "https://github.com/Roxicaro/Mining_Incremental/blob/main/PrintScreens/gameplay.gif"></img>

## 💻 Installation
```bash
# Clone and run
git clone https://github.com/Roxicaro/mining_incremental.git
cd mining_incremental
pip install -r requirements.txt
python main.py
```

## 🛠️ Building Distributions
```bash
# Windows EXE
pyinstaller --onefile --add-data "player_design.py;." --add-data "rock_design.py;." --add-data "command_list.py;." --add-data "ascii_designs.py;." main.py
```

## 📜 License
This game is **open-source** under the [GPL-3.0 License](LICENSE).  
- ✅ You can modify/sell copies  
- 🔓 Must include source code  
- 📝 See [NOTICE.md](NOTICE.md) for third-party credits

### Third-Party Dependencies
- [scrap-engine](https://github.com/lxgr-linux/scrap-engine) (GPL-3.0)

**Copyright** © 2025 Icaro Alves ([@Roxicaro](https://github.com/Roxicaro))


