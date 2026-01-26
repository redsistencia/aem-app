import type { Activity } from '$lib/types/activity';

export const activities: Activity[] = [
	{
		slug: 'mateada-comunitaria',
		date: '2025-03-10',
		title: 'Mateada comunitaria',
		description:
			'Encuentro abierto para compartir mates, charlas y fortalecer la comunidad argentina en Mallorca.',
		instagramUrl: 'https://www.instagram.com/p/DRcEnWJjKos/',
		sent: true
	},
	{
		slug: 'encuentro-memoria',
		date: '2025-04-02',
		title: 'Encuentro por la memoria',
		description:
			'Somos la semilla transoceánica que sembraron las Madres y las Abuelas, y brotamos orgullosxs, sabiéndonos más que ellxs, y que aunque quieran cortar todas las flores, nunca, NUNCA, podrán detener la primavera.',
		instagramUrl: 'https://www.instagram.com/p/DHOB5ICsUPg/',
		sent: false
	},
	{
		slug: 'roges-zurdos',
		date: '2025-04-02',
		title: 'Roges, zurdos, vagas i maleantes',
		description:
			'El viernes pasado, nos invitaron a participar en Roges, zurdos, vagas i maleantes. Un evento antifascista que contó con la participación de varios colectivos que resisten el avance de la ultraderecha y el fascismo en España y Argentina. Milei no solo siembra odio, racismo, homofobia y xenofobia, creando división entre les argentines, sino que, cuando termine su estafa, dejará un país endeudado y empobrecido , con alto desempleo y una industria destruida.¡pero nos levantaremos! Somos les herederes de las abuelas y madres de Plaza de Mayo, y de ellas aprendimos a luchar con amor y ternura, pero también con fuerza y convicción, sabiendo que estamos del lado correcto de la historia. ¡Fascismo NUNCA MÁS!',
		sent: false
	}
];
