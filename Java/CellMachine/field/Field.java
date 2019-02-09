package field;

import cell.Cell;

import java.util.ArrayList;

public class Field {
    private int width;
    private int height;
    private Cell[][] field; //相当于每格是存放Cell对象的

    public Field(int width, int height) {  // 创建构造函数
        this.width = width;
        this.height = height;
        field = new Cell[height][width];
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public void place(int row, int col, Cell cell) {
        field[row][col] = cell;
    }

    public Cell get(int row, int col) {
        return field[row][col];
    }

    public Cell[] getNeighbour(int row, int col) {
        ArrayList<Cell> neighs = new ArrayList<Cell>();
        for (int i = -1; i < 2; i++) {
            for (int j = -1; j < 2; j++) {
                int r = row + i;
                int c = col + j;
                if (r > -1 && c > -1 && r < height && c < width && !(r == row && c==col)) {
                    neighs.add(field[r][c]);
                }
            }
        }
        return neighs.toArray(new Cell[neighs.size()]);
    }

    public void clear() {
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                field[i][j] = null;
            }
        }
    }

    public static void main(String[] args) {
        Field field = new Field(30, 30);
        System.out.print(field.getNeighbour(10, 10).length);
    }
}