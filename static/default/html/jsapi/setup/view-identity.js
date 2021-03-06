// Setup View
var IdentityView = Backbone.View.extend(
{
    initialize: function() {
  		this.render();
    },
    render: function(){},
    events: {
      "click #btn-setup-passphrase"          : "processPassphrase",
    	"click #btn-setup-basic-info"          : "processBasic",
      "click #btn-setup-crypto-import"       : "processCryptoImport",
    	"click #btn-setup-source-settings"     : "processSourceSettings",
    	"click #btn-setup-source-local-import" : "processSourceImport"
    },
    showIndex: function() {
      this.$el.html(_.template($("#template-setup-welcome").html()));
    },
    showPassphrase: function() {
      $('#setup-progress').find('')
      this.$el.html(_.template($('#template-setup-passphrase').html()));
    },
    showProfiles: function() {
      this.$el.html(_.template($('#template-setup-profiles').html()));
    },
    showDiscovery: function() {
      this.$el.html(_.template($("#template-setup-discovery").html()));
      $('#demo-setup-discovery-action').delay(1500).fadeIn('normal');
    },
    showCryptoGenerated: function() {
      this.$el.html(_.template($('#template-setup-crypto-generated').html(), CryptoModel.attributes));
    },
    showSourceSettings: function() {
      this.$el.html(_.template($('#template-setup-source-local-settings').html(), SourceModel.attributes));      
    },
    showSourceLocal: function() {
      this.$el.html(_.template($('#template-setup-source-local').html(), SourceModel.attributes));      
    },
    showSourceRemoteChoose: function() {
      this.$el.html(_.template($('#template-setup-source-remote-choose').html(), {}));      
    },
    processPassphrase: function(e) {
      e.preventDefault();

      // Validate

      var passphrase_data = $('#form-setup-passphrase').serialize();
      console.log(passphrase_data);
      Mailpile.API.setup_crypto(passphrase_data, function(result) {
        console.log(result);

        if (result.status == 'success') {
          Backbone.history.navigate('#profiles', true);
        }
        else if (result.status == 'error' && result.error.invalid_passphrase) {
          
          $('#identity-vault-lock').find('.icon-lock-closed').addClass('color-12-red bounce');
          Mailpile.notification(result.status, result.message);

        }

      });
    },
    processProfileAdd: function(e) {

      e.preventDefault();

      // Process Data (will want to use a validation plugin)
      var basic_data = {};
      _.each($('#form-setup-basic-info').serializeArray(), function(element){
        var value = _.values(element);
        basic_data[value[0]] = value[1];
      });

      // Update Model
      SetupModel.set(basic_data);

      Backbone.history.navigate('#crypto-generated', true);

      // Update URL & View
      Backbone.history.navigate('#discovery', true);
  	},
    processCryptoImport: function(e) {
      alert('Prolly want to have to some "importing all the strong crypto maths feedback / progress thingy here before proceeding"');
      e.preventDefault();
      Backbone.history.navigate('#source-settings', true);
    }
});