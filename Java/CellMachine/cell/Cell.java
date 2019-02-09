package cell;

import java.awt.Graphics;

public class Cell {
    private boolean alive = false;

    public void reborn() { alive=true; }
    public boolean isAlive() { return alive; }
    public void die() { alive=false; }

    public void draw(Graphics g, int row, int col, int size) {
        g.drawRect(row,col,size,size);
        if(alive){
            g.fillRect(row,col,size,size);
        }
    }
    //  Functions()..
}
