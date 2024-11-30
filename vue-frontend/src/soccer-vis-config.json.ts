export class SoccerVisConfigJson {
    public static soccerFieldDimensions = {
        width_m: 105,
        height_m: 68
    };
    public static pixel_scaling_factor_soccer_field = 8;
    public static pcanvas_border_buffer_px = 25;
    public static canvasDimensions = {
        width_px: 890, // width_m * scaling_factor + 2 * border_buffer
        height_px: 594
    };

}