// I'm sorry people who actually know how to use React
// I'm bad at this and just wanted shared variables umu

export default class GlobalState {
    public static player_character: any = null;
    public static player_list: any = null;
    public static player_portaits: string[] = [];

    public static mod_from_total(total: number) {
        return Math.floor((total - 10) / 2)
    }
}