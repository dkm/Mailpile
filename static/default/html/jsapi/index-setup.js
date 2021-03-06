/* JS App Files */
{% include("jsapi/setup/model.js") %}
{% include("jsapi/setup/view-identity.js") %}
{% include("jsapi/setup/view-organize.js") %}
{% include("jsapi/setup/view-advanced.js") %}
{% include("jsapi/setup/router.js") %}

var SetupApp = (function ($, Backbone, global) {

    var init = function() {

      // Model
      global.SetupModel = new SetupModel();
      global.CryptoModel = new CryptoModel();
      global.SourceModel = new SourceModel();

      // Views
      global.IdentityView = new IdentityView({ el: $('#setup') });
      global.OrganizeView = new OrganizeView({ el: $('#setup') });
      global.AdvancedView = new AdvancedView({ el: $('#setup') });

  		// Router
  		global.Router = new SetupRouter($('#setup'));

      // Start Backbone History
      Backbone.history.start();
    };

    return { init: init };

} (jQuery, Backbone, window));
