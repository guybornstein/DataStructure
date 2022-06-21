import java.util.Random;

public class AQPHashTable extends OAHashTable {

	private ModHash func;

	public AQPHashTable(int m, long p) {
		super(m);
		this.func = ModHash.GetFunc(m, p);
	}
	
	@Override
	public int Hash(long x, int i) {
		return (((func.Hash(x) + (int)(Math.pow(-1, i%2))*((int)Math.pow(i, 2))) % size)+ size) % size;

	}
}
