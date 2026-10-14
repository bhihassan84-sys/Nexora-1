const $ = id => document.getElementById(id);
const button = $("refresh");
function setMessage(text, error=false){$("message").textContent=text;$("message").classList.toggle("error",error);}
function paint(data){
  const side=data.signal||"NO SIGNAL";
  $("signal").innerHTML=side==="NO SIGNAL"?"NO<br>SIGNAL":side;
  $("headline").textContent=side==="BUY"?"Bullish setup":side==="SELL"?"Bearish setup":"No clear setup";
  $("reason").textContent=data.reason||data.error||"No explanation provided.";
  $("confidence").textContent=side==="NO SIGNAL"?"—":`${data.confidence ?? 0}%`;
  $("meter").style.width=`${side==="NO SIGNAL"?0:(data.confidence||0)}%`;
  $("orb").classList.toggle("buy",side==="BUY");
  $("market").textContent=data.symbol||$("symbol").value;
  $("candle-count").textContent=`Candles: ${data.candles ?? "—"}`;
  const x=data.indicators||{};
  $("rsi").textContent=x.rsi14==null?"—":x.rsi14;
  $("ema").textContent=x.ema9==null?"—":`${x.ema9} / ${x.ema21} / ${x.ema50}`;
  $("updated").textContent=data.updated_at?new Date(data.updated_at).toLocaleTimeString():"—";
  const b=data.backtest||{};
  $("bt-signals").textContent=b.signals??"—";
  $("bt-wins").textContent=b.wins??"—";
  $("bt-rate").textContent=b.win_rate_pct==null?"—":`${b.win_rate_pct}%`;
}
button.addEventListener("click",async()=>{
  button.disabled=true;button.textContent="FETCHING CANDLES…";setMessage("Requesting historical data from the configured API…");
  try{
    const response=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({symbol:$("symbol").value.trim()})});
    const data=await response.json();paint(data);
    if(!response.ok) setMessage(data.error||"Could not analyze market.",true);
    else setMessage(`Analysis complete. Received ${data.candles} candles. Check the evaluation caveats below.`);
  }catch(e){setMessage("Cannot reach the local server. Start it from the project folder and try again.",true);}
  finally{button.disabled=false;button.textContent="ANALYZE MARKET ↗";}
});
fetch("/api/status").then(r=>r.json()).then(paint).catch(()=>{});
