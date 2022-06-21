import java.util.Random;

public class QPHashTable extends OAHashTable {

	private ModHash func;


	public QPHashTable(int m, long p) {
		super(m);
		this.func = ModHash.GetFunc(m, p);
	}
	
	@Override
	public int Hash(long x, int i) {
		return (func.Hash(x) + (int)Math.pow(i, 2)) % size;
	}
}
