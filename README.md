# Funny Granny ! 
### Jeanne Leclere · Rayane Boukef · Edouard Castignoli · Erwann Briot · Tom Hausmann


---
<img width="960" alt="Funny Granny screen" src="https://github.com/user-attachments/assets/f5d2b09a-23d5-4593-8acd-bd724409d5b3" />
---


## About the Project

**Funny Granny** is a  2D 2-player game where grandpas and grandmas settle their conflict once and for all ! Designed for players aged 6 to 99, the game showcases two teams against each other s using a hilarious arsenal: toilet paper rolls, jam jars, canes, and glasses. Win by knocking out the opposing team three times, all set in a light-hearted, pixel art world inspired by classics like *Worms* .

<br/>

## Table of Contents

- [About the Project](#about-the-project)
- [Team](#team)
- [Features](#features)
- [Development Process](#development-process)
- [Roles & Responsibilities](#roles--responsibilities)
- [Art & Design](#art--design)
- [How to Run](#how-to-run)
- [Planned Improvements](#planned-improvements)

---

## Team

| Name               | Role                              |
|--------------------|-----------------------------------|
| Jeanne Leclere     | Player Management                 |
| Rayane Boukef      | Weapon Management                 |
| Edouard Castignoli | Collision Management              |
| Erwann Briot       | Project Management                |
| Tom Hausmann       | Artistic Direction (Art & UI)     |

---

## Features

- **2D Pixel Art Platformer**: Accessible for kids and nostalgic for adults!
- **Unique Characters**: Play as grandmas or grandpas, each with their own animations.
- **Hilarious Weapons**: Choose from oddball weapons like jam jars and canes.
- **Local Multiplayer**: Two players, one epic (and silly) fight.
- **Custom Levels**: Hand-crafted stages filled with colorful obstacles.

---

## Development Process

The game was developed through several collaborative brainstorming and coding sessions:
- **Brainstorming**: Initially considered a golf game, we pivoted for originality to create Funny Granny.
- **Prototyping**: Early test versions focused on core mechanics like walking, jumping, trajectory, and collisions.
- **Session Coding**: Tasks distributed by specialization to ensure each member contributed to their strengths.
- **Integration**: Multiple challenges in merging everyone’s code; overcome by organizing files, assets, and comments.
- **Polish & Pitch**: Level design, music, and rehearsing a fun pitch presentation rounded out the process.

**Major Challenges**:  
- Map collision accuracy and cross-platform file handling.
- Merging code from various OS environments (Linux, macOS, Windows).
- Ensuring designs rendered correctly in-game.

---

## Roles & Responsibilities

**Player Management** (*Jeanne*):  
- Designed the Player class for grannies and grandpas.
- Managed animation, movement, and game logic for wins/losses.

**Weapon Management** (*Rayane*):  
- Implemented weapon functionality and projectile trajectories.

**Collision Management** (*Edouard*):  
- Built collision detection using invisible rectangles for platform boundaries.
- Debugged platform edge interactions.

**Project Management** (*Erwann*):  
- Oversaw integration, managed files, and bridged functional gaps among team members.

**Artistic Direction** (*Tom*):  
- Created a charming, consistent visual style using pixel art and vector design tools.
- Managed all assets, sprites, and backgrounds for both characters and levels.

---

## Art & Design

- **Visual Style**: Whimsical, cartoon-inspired pixel art to appeal to all ages.
- **Tools Used**: Figma for UI and sprites, Universal LPC Spritesheet Generator for character design.
- **Challenges**: Ensuring art assets fit and displayed correctly in-game across devices.

---

## How to Run

1. **Requirements**
   - [Python 3.x](https://www.python.org/)
   - [pygame](https://www.pygame.org/) library

2. **Installation**
   ```bash
   pip install pygame
   ```

3. **Running the Game**
   - Clone this repository.
   - Ensure all assets are in the correct folders.
   - Run the main file:
     ```bash
     python main.py
     ```

---

## Planned Improvements

- Display the currently equipped weapon for each player.
- Implement an inventory UI for both teams.
- Add an animated "ready" screen.
- Enhance the weapon trajectory visuals.

---

## Acknowledgements

Special thanks to everyone who offered feedback !

---

*We hope Funny Granny brings as many laughs to you as it did to our team building it!*




**NB : AI was used to format this README in markdown, so that it is more pleasing to read !**
