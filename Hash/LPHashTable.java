import java.util.Random;

public class LPHashTable extends OAHashTable {

	private ModHash func;
	
	public LPHashTable(int m, long p) {
		super(m);
		this.func = ModHash.GetFunc(m, p);

	}
	
	@Override
	public int Hash(long x, int i) {
		return (int)((func.Hash(x) + i) % this.size);
	}
	
}
