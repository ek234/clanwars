
# Clan Wars

This is CLI based game tightly based on the game Clash of Clans. You control Troops ~invading~ freeing a foreign village.

There are a total of 3 rounds. You need to ~destroy~ renovate all non-wall structures to win a round. Your infantry refills after each win. Of all the troops, you can choose to play as either the King or the Archer Queen. All other troops are automatic- you can only control their spawn. Players can choose from 3 spawn points.

## Troops

The Troops that are available to you are :

```
king:
  maxhealth: 200
  range: 5
  damage: 25
  speed: 2
  size:
    x: 3
    y: 2
```

You can control the King with 'w/a/s/d'. Switch between weapons sword and Levithan axe (with AoE) with key 'e'. And attack with '<space>' key.

```
queen:
  maxhealth: 200
  range: 8
  radius: 2
  erange: 16
  eradius: 4
  damage: 15
  speed: 4
  size:
    x: 3
    y: 2
```

You can control the Queen with 'w/a/s/d'. Attack using a volley of arrows (AoE) with '<space>' key. Use Queen's special eagle arrow with 'e' ( lands after 1s with large AoE ).

```
barbarian:
  maxhealth: 50
  damage: 16
  speed: 1
  size:
    x: 1
    y: 2
  maxnum: 10
```

Automated troop with given specifications.

```
archer:
  maxhealth: 25
  damage: 8
  speed: 2
  range: 9
  size:
    x: 1
    y: 2
  maxnum: 2
```

Automated troop with given specifications. Can attack over walls and buildings. Okay isn't archer way too OP with that sorta range.

```
ballon:
  maxhealth: 50
  damage: 32
  speed: 2
  size:
    x: 1
    y: 2
  maxnum: 3
```

Automated troop with given specifications. Ariel troop - is not affected by cannons. These destroy all defensive buildings first and then attack other buildings.

## Structures

```
townhall:
  maxhealth: 300
  size:
    x: 4
    y: 3

```

Central building with no purpose. Looks like an outhouse.

```
hut:
  maxhealth: 100
  size:
    x: 2
    y: 2

```

Huts- where the villagers live. They are sleeping rn tho.

```
cannon:
  maxhealth: 100
  size:
    x: 3
    y: 1
  range: 8
  damage: 5
```

Boom Boom!! Attack once every 2 timesteps towards any enemy in its range.

```
tower:
  maxhealth: 200
  size:
    x: 4
    y: 3
  range: 8
  radius: 1
  damage: 5
```

Vizz! Target once every 3 timesteps at an enemy in range and attack an AoE around it.

```
wall:
  maxhealth: 30
  size:
    x: 1
    y: 1
```

Boring block. *Must avoid*. Maybe bfs can help or maybe we'll have to resort to a star.

## Spells

- Heal Spell
Increase the health of all troops by 50%.

- Rage Spell
Increase speed and damage of all troops for a limited amount of time ( 5 timesteps ).

- Rise Spell
Reanimate dead troops with low (10%) health.

## display
```
display:
  size:
    x: 100
    y: 25
  unitsize:
    x: 1
    y: 1
  fps: 10
```

### Note: press '[' only if you are a n00b
