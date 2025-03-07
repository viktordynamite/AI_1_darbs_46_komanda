# Spēles apraksts

## Papildu prasības programmatūrai
Spēles sākumā cilvēks-spēlētājs norāda spēlē izmantojamas simbolu virknes garumu, kas var būt diapazonā no 15 līdz 25 simboliem. Spēles programmatūra gadījuma ceļā saģenerē simbolu virkni atbilstoši uzdotajam garumam, tajā iekļaujot X un O simbolus.

## Spēles noteikumi
Spēles sākumā ir dota ģenerētā simbolu virkne. Katram spēlētājam ir 0 punktu. Viens spēlētājs spēlē ar apļiem, otrs – ar krustiņiem. Spēli uzsāk spēlētājs, kas spēlē ar aplīšiem.

- **Spēlētājs ar aplīšiem (O):**
  - Drīkst aizvietot divus blakusstāvošus krustiņus ar aplīti (**XX → O**) un iegūt **2 punktus**.
  - Drīkst aizvietot krustiņu un aplīti, kas stāv blakus, ar aplīti (**XO → O**) un iegūt **1 punktu**.

- **Spēlētājs ar krustiņiem (X):**
  - Drīkst aizvietot divus aplīšus ar krustiņu (**OO → X**) un iegūt **2 punktus**.
  - Drīkst aizvietot aplīti un krustiņu ar krustiņu (**OX → X**) un iegūt **1 punktu**.

Spēle beidzas, kad kāds no spēlētājiem nevar izdarīt gājienu, vai simbolu virknē ir palikusi tikai viena figūra. Uzvar spēlētājs, kam spēles beigās ir vairāk punktu.
